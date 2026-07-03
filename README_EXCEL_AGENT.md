# 🤖 AI Excel Cleaning Agent (Approach 2)

An intelligent AI-powered Excel data cleaning agent that uses GPT-4 to analyze data quality issues and generate custom cleaning code automatically.

## ✨ Features

- **🔍 AI Data Quality Analysis**: Automatically analyzes your Excel data and identifies issues
- **🤖 Auto-Clean Mode**: Iteratively cleans data with AI recommendations
- **💬 Natural Language Instructions**: Clean data using plain English commands
- **🔧 Code Generation**: AI generates and executes custom pandas code
- **📊 Detailed Reports**: Get comprehensive cleaning operation reports
- **👁️ Preview Changes**: See before/after comparisons
- **⚡ Production-Ready**: Handles edge cases and large datasets

## 📋 What It Can Do

### Data Quality Analysis
- Detect duplicates, missing values, and data type mismatches
- Identify whitespace/formatting issues
- Spot inconsistent values and invalid patterns
- Generate severity-based issue reports

### Cleaning Operations
- Remove duplicate rows
- Delete empty rows/columns
- Trim whitespace
- Standardize text formatting
- Fix data types
- Fill missing values
- And much more via natural language!

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/SparerBow/EvidentiaAI.git
cd EvidentiaAI

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
# Create a .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Or set it as an environment variable:
```bash
export OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Agent

```bash
# Interactive mode
python ai_excel_agent.py

# Or pass file path as argument
python ai_excel_agent.py data.xlsx
```

## 💡 Usage Examples

### Example 1: Analyze Data Quality

```bash
$ python ai_excel_agent.py
📁 Enter Excel file path: sales_data.xlsx

Select option (1-7): 1
```

**Output:**
```
🔍 Analyzing data quality...

📊 DATA QUALITY ANALYSIS REPORT
================================================================================
Data Quality Score: 45/100

🚨 ISSUES FOUND:

🔴 [HIGH] 1,245 duplicate records found
   Description: Multiple identical rows across customer data
   Columns: customer_id, email, phone

🟡 [MEDIUM] 312 missing email addresses
   Description: Email column has NULL values
   Columns: email

🟢 [LOW] Inconsistent phone number formatting
   Description: Mix of (555) 123-4567 and 555-123-4567 formats
   Columns: phone

💡 RECOMMENDED ACTIONS:

1. Remove duplicate rows based on customer_id (Priority: 9/10)
   Reasoning: Duplicates cause data integrity issues

2. Fill or remove rows with missing email addresses (Priority: 8/10)
   Reasoning: Email is critical for communication
```

### Example 2: Auto-Clean with AI

```python
from ai_excel_agent import AIExcelCleaningAgent

agent = AIExcelCleaningAgent('messy_data.xlsx')
agent.auto_clean(max_iterations=5)
agent.save('cleaned_data.xlsx')
```

### Example 3: Custom Cleaning Instructions

```python
agent = AIExcelCleaningAgent('data.xlsx')

# Clean with natural language
agent.clean_by_instruction("Remove duplicates and standardize email formats")
agent.clean_by_instruction("Fill missing phone numbers with 'N/A'")
agent.clean_by_instruction("Convert all dates to YYYY-MM-DD format")

agent.preview_changes()
agent.save('cleaned_data.xlsx')
```

### Example 4: Get Detailed Report

```python
agent = AIExcelCleaningAgent('data.xlsx')
agent.clean_by_instruction("Remove rows with missing critical fields")

report = agent.get_report()
print(report)
```

**Output:**
```json
{
  "file": "data.xlsx",
  "original_rows": 10000,
  "final_rows": 9245,
  "original_columns": 15,
  "final_columns": 15,
  "issues_found": 8,
  "operations": [
    {
      "instruction": "Remove rows with missing critical fields",
      "status": "success"
    }
  ]
}
```

## 🎯 Interactive Menu Options

When running `python ai_excel_agent.py`, you'll see this menu:

```
1. Analyze data quality        - AI analyzes your data for issues
2. Auto-clean                  - Automated cleaning with AI recommendations
3. Custom instruction          - Enter your own cleaning command
4. Preview changes             - See before/after comparison
5. Save cleaned file           - Save the cleaned Excel file
6. Get report                  - View detailed cleaning report
7. Exit                        - Close the agent
```

## 🔧 Advanced Usage

### Custom Cleaning Pipeline

```python
from ai_excel_agent import AIExcelCleaningAgent

agent = AIExcelCleaningAgent('data.xlsx', api_key='your-api-key')

# Chain operations
(agent
    .analyze_data_quality()
    .clean_by_instruction("Remove duplicates")
    .clean_by_instruction("Standardize all text to lowercase")
    .clean_by_instruction("Remove special characters from phone numbers")
    .preview_changes()
    .save('final_cleaned.xlsx')
)

# Get comprehensive report
report = agent.get_report()
```

### Batch Processing

```python
import glob

files = glob.glob('data/*.xlsx')

for file in files:
    print(f"\n📁 Processing {file}...")
    agent = AIExcelCleaningAgent(file)
    agent.auto_clean()
    agent.save(f'cleaned/{file}')
```

## 📊 Supported Excel Formats

- `.xlsx` (Excel 2010+)
- `.xls` (Excel 97-2003) - via openpyxl

## 🛡️ Safety Features

- ✅ Preserves original file (creates new file with `_cleaned` suffix)
- ✅ Shows generated code before execution
- ✅ Validates all operations before applying
- ✅ Includes error handling and rollback

## 🔑 Requirements

- Python 3.8+
- OpenAI API key (GPT-4 access)
- pandas >= 1.3.0
- openpyxl >= 3.7.0
- openai >= 0.27.0

## 📦 Installation from Source

```bash
git clone https://github.com/SparerBow/EvidentiaAI.git
cd EvidentiaAI
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use in your projects

## 🆘 Troubleshooting

### "OPENAI_API_KEY not found"
```bash
# Set your API key
export OPENAI_API_KEY=sk-your-key-here
```

### "File not found"
Make sure the Excel file path is correct and the file exists in the current directory or provide full path.

### "Rate limit exceeded"
The OpenAI API has rate limits. Wait a moment and try again, or upgrade your API plan.

## 📧 Support

For issues or questions, please open a GitHub issue or contact the maintainers.

## 🚀 What's Next?

- [ ] Support for CSV files
- [ ] Batch processing from directory
- [ ] Custom validation rules
- [ ] Data profiling reports
- [ ] Integration with databases
- [ ] Web UI dashboard

---

**Built with ❤️ using AI and Python**
