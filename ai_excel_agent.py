import pandas as pd
import openai
import json
import sys
import os
from pathlib import Path

class AIExcelCleaningAgent:
    """
    AI-powered Excel cleaning agent that uses LLM to intelligently clean data.
    Analyzes data quality issues and generates custom cleaning code.
    """
    
    def __init__(self, file_path, api_key=None):
        """
        Initialize the AI Excel Cleaning Agent
        
        Args:
            file_path (str): Path to the Excel file to clean
            api_key (str): OpenAI API key (if None, uses OPENAI_API_KEY env variable)
        """
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        self.original_df = self.df.copy()
        
        # Set API key
        if api_key:
            openai.api_key = api_key
        elif not openai.api_key:
            openai.api_key = os.getenv('OPENAI_API_KEY')
        
        self.cleaning_log = []
        self.stats = {
            'original_rows': len(self.df),
            'original_columns': len(self.df.columns),
            'issues_found': 0
        }
    
    def analyze_data_quality(self):
        """Use AI to analyze data quality issues"""
        print("\n🔍 Analyzing data quality...\n")
        
        # Prepare data summary
        sample = self.df.head(10).to_string()
        column_info = {
            "columns": self.df.columns.tolist(),
            "shape": list(self.df.shape),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicate_rows": self.df.duplicated().sum()
        }
        
        prompt = f"""
You are a data quality expert. Analyze this Excel dataset and identify ALL cleaning issues.

Dataset Info:
{json.dumps(column_info, indent=2)}

Sample Data (first 10 rows):
{sample}

Provide a detailed JSON response with this exact structure:
{{
    "issues": [
        {{
            "issue": "issue name",
            "severity": "high/medium/low",
            "description": "detailed description",
            "affected_columns": ["col1", "col2"]
        }}
    ],
    "recommended_actions": [
        {{
            "action": "action description",
            "priority": 1-10,
            "reasoning": "why this is needed"
        }}
    ],
    "data_quality_score": 0-100,
    "critical_issues": ["issue1", "issue2"]
}}

Be thorough and identify:
- Duplicates
- Missing values
- Data type mismatches
- Whitespace/formatting issues
- Inconsistent values
- Invalid data patterns
"""
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        try:
            analysis = json.loads(response['choices'][0]['message']['content'])
            self.stats['issues_found'] = len(analysis['issues'])
            
            print("=" * 80)
            print("📊 DATA QUALITY ANALYSIS REPORT")
            print("=" * 80)
            print(f"\nData Quality Score: {analysis['data_quality_score']}/100\n")
            
            print("🚨 ISSUES FOUND:")
            for issue in analysis['issues']:
                severity_icon = "🔴" if issue['severity'] == 'high' else "🟡" if issue['severity'] == 'medium' else "🟢"
                print(f"\n{severity_icon} [{issue['severity'].upper()}] {issue['issue']}")
                print(f"   Description: {issue['description']}")
                print(f"   Columns: {', '.join(issue['affected_columns'])}")
            
            print("\n\n💡 RECOMMENDED ACTIONS:")
            for i, action in enumerate(analysis['recommended_actions'], 1):
                print(f"\n{i}. {action['action']} (Priority: {action['priority']}/10)")
                print(f"   Reasoning: {action['reasoning']}")
            
            if analysis['critical_issues']:
                print(f"\n\n⚠️  CRITICAL ISSUES TO ADDRESS:")
                for issue in analysis['critical_issues']:
                    print(f"   - {issue}")
            
            print("\n" + "=" * 80)
            
            return analysis
        except json.JSONDecodeError:
            print("❌ Failed to parse AI response")
            return None
    
    def clean_by_instruction(self, instruction):
        """
        Clean data based on natural language instruction
        
        Args:
            instruction (str): Natural language instruction for cleaning
        """
        print(f"\n📝 Cleaning Instruction: {instruction}\n")
        
        column_info = {
            "columns": self.df.columns.tolist(),
            "shape": list(self.df.shape),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        }
        
        prompt = f"""
You are a pandas expert. Generate ONLY valid Python code to clean this Excel dataset.

Dataset Info:
{json.dumps(column_info, indent=2)}

Current dataframe shape: {self.df.shape}

User's cleaning instruction: {instruction}

Generate clean, production-ready Python pandas code that:
1. Performs the requested cleaning
2. Uses 'df' as the variable name
3. Is efficient and handles edge cases
4. Includes comments explaining each step
5. Does NOT include import statements
6. Does NOT include df.head(), print(), or display statements

Return ONLY the code, starting with ```python and ending with ```
"""
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        code_response = response['choices'][0]['message']['content']
        
        # Extract code from markdown
        code = code_response.replace('```python', '').replace('```', '').strip()
        
        print(f"🔧 Generated cleaning code:\n")
        print("-" * 80)
        print(code)
        print("-" * 80 + "\n")
        
        try:
            # Execute the cleaning code
            exec_globals = {'df': self.df, 'pd': pd}
            exec(code, exec_globals)
            self.df = exec_globals['df']
            
            print(f"✅ Successfully applied: {instruction}")
            self.cleaning_log.append({
                'instruction': instruction,
                'code': code,
                'status': 'success'
            })
            
            # Show stats
            rows_removed = self.stats['original_rows'] - len(self.df)
            if rows_removed > 0:
                print(f"   📊 Rows removed: {rows_removed}")
            print(f"   📊 Current shape: {self.df.shape}")
            
        except Exception as e:
            print(f"❌ Error applying instruction: {str(e)}")
            self.cleaning_log.append({
                'instruction': instruction,
                'code': code,
                'status': 'failed',
                'error': str(e)
            })
            raise
    
    def auto_clean(self, max_iterations=5):
        """
        Automatically clean the dataset using AI analysis
        
        Args:
            max_iterations (int): Maximum number of cleaning iterations
        """
        print("\n🤖 STARTING AUTO-CLEAN MODE\n")
        
        for iteration in range(max_iterations):
            print(f"\n{'='*80}")
            print(f"AUTO-CLEAN ITERATION {iteration + 1}/{max_iterations}")
            print(f"{'='*80}\n")
            
            analysis = self.analyze_data_quality()
            
            if not analysis or analysis['data_quality_score'] >= 95:
                print("\n✨ Data quality is excellent! Cleaning complete.\n")
                break
            
            # Get top priority action
            if analysis['recommended_actions']:
                top_action = sorted(analysis['recommended_actions'], 
                                   key=lambda x: x['priority'], reverse=True)[0]
                
                input("\n⏸️  Press Enter to apply the next recommended action...")
                self.clean_by_instruction(top_action['action'])
    
    def preview_changes(self):
        """Show a preview of changes made"""
        print("\n" + "=" * 80)
        print("📋 CLEANING PREVIEW")
        print("=" * 80)
        
        print(f"\nOriginal Data:")
        print(f"  • Rows: {self.stats['original_rows']}")
        print(f"  • Columns: {self.stats['original_columns']}")
        
        print(f"\nCleaned Data:")
        print(f"  • Rows: {len(self.df)}")
        print(f"  • Columns: {len(self.df.columns)}")
        
        print(f"\nChanges:")
        print(f"  • Rows removed: {self.stats['original_rows'] - len(self.df)}")
        print(f"  • Columns removed: {self.stats['original_columns'] - len(self.df.columns)}")
        
        print(f"\n\nFirst 10 rows of cleaned data:")
        print(self.df.head(10).to_string())
    
    def save(self, output_path=None):
        """
        Save cleaned data to Excel
        
        Args:
            output_path (str): Path to save cleaned file (default: original_cleaned.xlsx)
        """
        if output_path is None:
            output_path = str(Path(self.file_path).stem) + '_cleaned.xlsx'
        
        self.df.to_excel(output_path, index=False)
        
        print("\n" + "=" * 80)
        print("💾 SAVE REPORT")
        print("=" * 80)
        print(f"\n✅ Cleaned file saved to: {output_path}")
        print(f"   • Final rows: {len(self.df)}")
        print(f"   • Final columns: {len(self.df.columns)}")
        
        if self.cleaning_log:
            print(f"\n📝 Cleaning operations performed ({len(self.cleaning_log)}):")
            for i, log in enumerate(self.cleaning_log, 1):
                status_icon = "✅" if log['status'] == 'success' else "❌"
                print(f"   {status_icon} {i}. {log['instruction']}")
        
        print("=" * 80 + "\n")
        return output_path
    
    def get_report(self):
        """Get a summary report of all cleaning operations"""
        return {
            'file': self.file_path,
            'original_rows': self.stats['original_rows'],
            'final_rows': len(self.df),
            'original_columns': self.stats['original_columns'],
            'final_columns': len(self.df.columns),
            'issues_found': self.stats['issues_found'],
            'operations': self.cleaning_log
        }


# Example usage and CLI interface
if __name__ == "__main__":
    
    print("\n" + "=" * 80)
    print("🤖 AI EXCEL CLEANING AGENT")
    print("=" * 80)
    
    # Get file path from user
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("\n📁 Enter Excel file path: ").strip()
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    # Initialize agent
    agent = AIExcelCleaningAgent(file_path)
    
    # Main menu
    while True:
        print("\n" + "-" * 80)
        print("MAIN MENU")
        print("-" * 80)
        print("1. Analyze data quality")
        print("2. Auto-clean (AI recommendations)")
        print("3. Custom cleaning instruction")
        print("4. Preview changes")
        print("5. Save cleaned file")
        print("6. Get report")
        print("7. Exit")
        print("-" * 80)
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            agent.analyze_data_quality()
        
        elif choice == "2":
            agent.auto_clean()
        
        elif choice == "3":
            instruction = input("\n📝 Enter cleaning instruction: ").strip()
            if instruction:
                agent.clean_by_instruction(instruction)
        
        elif choice == "4":
            agent.preview_changes()
        
        elif choice == "5":
            output = input("📁 Enter output file path (press Enter for default): ").strip()
            agent.save(output if output else None)
        
        elif choice == "6":
            report = agent.get_report()
            print("\n" + "=" * 80)
            print("📊 CLEANING REPORT")
            print("=" * 80)
            print(json.dumps(report, indent=2))
        
        elif choice == "7":
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("❌ Invalid option. Please try again.")
