"""
Example usage of the AI Excel Cleaning Agent
"""

from ai_excel_agent import AIExcelCleaningAgent
import os

# Make sure to set your OpenAI API key
# export OPENAI_API_KEY=your_api_key_here

def example_1_analyze_quality():
    """Example 1: Analyze data quality"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Analyze Data Quality")
    print("="*80)
    
    # Initialize agent with your Excel file
    agent = AIExcelCleaningAgent('sample_data.xlsx')
    
    # Analyze data quality
    analysis = agent.analyze_data_quality()
    
    return agent


def example_2_auto_clean():
    """Example 2: Auto-clean with AI recommendations"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Auto-Clean Mode")
    print("="*80)
    
    agent = AIExcelCleaningAgent('sample_data.xlsx')
    
    # Run auto-clean (iterative with user confirmation)
    agent.auto_clean(max_iterations=3)
    
    # Preview and save
    agent.preview_changes()
    agent.save('sample_data_auto_cleaned.xlsx')
    
    return agent


def example_3_custom_instructions():
    """Example 3: Custom cleaning instructions"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Custom Cleaning Instructions")
    print("="*80)
    
    agent = AIExcelCleaningAgent('sample_data.xlsx')
    
    # Apply custom cleaning instructions
    agent.clean_by_instruction("Remove all duplicate rows")
    agent.clean_by_instruction("Standardize all email addresses to lowercase")
    agent.clean_by_instruction("Remove any rows with missing critical fields")
    agent.clean_by_instruction("Trim whitespace from all text columns")
    
    agent.preview_changes()
    agent.save('sample_data_custom_cleaned.xlsx')
    
    return agent


def example_4_chained_operations():
    """Example 4: Chained operations"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Chained Operations")
    print("="*80)
    
    # You can chain operations together
    agent = AIExcelCleaningAgent('sample_data.xlsx')
    
    # Analyze first
    agent.analyze_data_quality()
    
    # Then clean with custom instructions
    agent.clean_by_instruction("Remove duplicate rows")
    agent.clean_by_instruction("Fill missing values with 'Unknown'")
    
    # Preview and save
    agent.preview_changes()
    agent.save('sample_data_final.xlsx')
    
    # Get report
    report = agent.get_report()
    print("\nCleaning Report:")
    print(report)
    
    return agent


def example_5_batch_processing():
    """Example 5: Batch processing multiple files"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Batch Processing")
    print("="*80)
    
    import glob
    
    # Process all Excel files in current directory
    excel_files = glob.glob('*.xlsx')
    
    for file in excel_files:
        if '_cleaned' not in file:  # Skip already cleaned files
            print(f"\n📁 Processing: {file}")
            
            try:
                agent = AIExcelCleaningAgent(file)
                
                # Quick analysis
                agent.analyze_data_quality()
                
                # Apply standard cleaning
                agent.clean_by_instruction("Remove duplicates and empty rows")
                
                # Save cleaned version
                output_file = file.replace('.xlsx', '_cleaned.xlsx')
                agent.save(output_file)
                
            except Exception as e:
                print(f"❌ Error processing {file}: {str(e)}")


def example_6_with_api_key():
    """Example 6: Using explicit API key"""
    print("\n" + "="*80)
    print("EXAMPLE 6: With Explicit API Key")
    print("="*80)
    
    # You can pass API key directly
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return
    
    agent = AIExcelCleaningAgent('sample_data.xlsx', api_key=api_key)
    
    # Run analysis and cleaning
    agent.analyze_data_quality()
    agent.clean_by_instruction("Remove all duplicates")
    agent.preview_changes()
    agent.save('sample_data_cleaned.xlsx')


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🤖 AI EXCEL CLEANING AGENT - EXAMPLES")
    print("="*80)
    
    print("\nAvailable Examples:")
    print("1. Analyze data quality")
    print("2. Auto-clean with AI recommendations")
    print("3. Custom cleaning instructions")
    print("4. Chained operations")
    print("5. Batch processing")
    print("6. Using explicit API key")
    
    choice = input("\nSelect example (1-6) or 'all' to run all: ").strip().lower()
    
    try:
        if choice == '1':
            example_1_analyze_quality()
        elif choice == '2':
            example_2_auto_clean()
        elif choice == '3':
            example_3_custom_instructions()
        elif choice == '4':
            example_4_chained_operations()
        elif choice == '5':
            example_5_batch_processing()
        elif choice == '6':
            example_6_with_api_key()
        elif choice == 'all':
            example_1_analyze_quality()
            example_3_custom_instructions()
            example_4_chained_operations()
        else:
            print("❌ Invalid choice")
    
    except FileNotFoundError:
        print("\n❌ Error: sample_data.xlsx not found")
        print("Please provide your own Excel file for testing")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
