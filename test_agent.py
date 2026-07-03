"""
Test suite for AI Excel Cleaning Agent
"""

import unittest
import pandas as pd
import os
from pathlib import Path
from ai_excel_agent import AIExcelCleaningAgent

class TestAIExcelCleaningAgent(unittest.TestCase):
    """Test cases for the AI Excel Cleaning Agent"""
    
    @classmethod
    def setUpClass(cls):
        """Create test data file"""
        # Create sample data with various quality issues
        test_data = {
            'Name': ['John Doe', 'Jane Smith', 'John Doe', '  Bob Jones  ', 'Alice Brown'],
            'Email': ['john@example.com', 'jane@example.com', 'john@example.com', None, 'alice@example.com'],
            'Phone': ['555-1234', '555-5678', '555-1234', '555-9012', None],
            'Age': [30, 25, 30, 35, 28],
            'Score': [85.5, None, 85.5, 92.0, 88.5]
        }
        
        df = pd.DataFrame(test_data)
        cls.test_file = 'test_data.xlsx'
        df.to_excel(cls.test_file, index=False)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test files"""
        for file in ['test_data.xlsx', 'test_data_cleaned.xlsx']:
            if os.path.exists(file):
                os.remove(file)
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = AIExcelCleaningAgent(self.test_file)
        
        self.assertIsNotNone(agent.df)
        self.assertEqual(agent.stats['original_rows'], 5)
        self.assertEqual(agent.stats['original_columns'], 5)
    
    def test_data_load(self):
        """Test Excel file loading"""
        agent = AIExcelCleaningAgent(self.test_file)
        
        self.assertIsInstance(agent.df, pd.DataFrame)
        self.assertEqual(len(agent.df), 5)
        self.assertEqual(len(agent.df.columns), 5)
    
    def test_get_report(self):
        """Test report generation"""
        agent = AIExcelCleaningAgent(self.test_file)
        report = agent.get_report()
        
        self.assertIn('file', report)
        self.assertIn('original_rows', report)
        self.assertIn('operations', report)
    
    def test_cleaning_log(self):
        """Test cleaning log tracking"""
        agent = AIExcelCleaningAgent(self.test_file)
        
        self.assertEqual(len(agent.cleaning_log), 0)
        
        # Note: This would require a valid OpenAI API key to test fully
        # agent.clean_by_instruction("Remove duplicates")
        # self.assertEqual(len(agent.cleaning_log), 1)


class TestDataQualityChecks(unittest.TestCase):
    """Test data quality checks"""
    
    def test_duplicate_detection(self):
        """Test duplicate row detection"""
        df = pd.DataFrame({
            'id': [1, 2, 2, 3],
            'name': ['a', 'b', 'b', 'c']
        })
        
        duplicates = df.duplicated().sum()
        self.assertEqual(duplicates, 1)
    
    def test_missing_value_detection(self):
        """Test missing value detection"""
        df = pd.DataFrame({
            'id': [1, 2, None, 4],
            'name': ['a', None, 'c', 'd']
        })
        
        missing = df.isnull().sum().sum()
        self.assertEqual(missing, 2)
    
    def test_whitespace_trimming(self):
        """Test whitespace trimming"""
        df = pd.DataFrame({
            'name': ['  John  ', '  Jane  ', 'Bob']
        })
        
        df['name'] = df['name'].str.strip()
        
        self.assertEqual(df['name'][0], 'John')
        self.assertEqual(df['name'][1], 'Jane')
        self.assertEqual(df['name'][2], 'Bob')


class TestPandasOperations(unittest.TestCase):
    """Test pandas cleaning operations"""
    
    def test_drop_duplicates(self):
        """Test dropping duplicate rows"""
        df = pd.DataFrame({
            'id': [1, 2, 2, 3],
            'value': ['a', 'b', 'b', 'c']
        })
        
        df_clean = df.drop_duplicates()
        
        self.assertEqual(len(df_clean), 3)
    
    def test_drop_empty_rows(self):
        """Test dropping empty rows"""
        df = pd.DataFrame({
            'col1': [1, None, 3],
            'col2': [None, None, 'c']
        })
        
        df_clean = df.dropna(how='all')
        
        self.assertEqual(len(df_clean), 3)
    
    def test_data_type_conversion(self):
        """Test data type conversion"""
        df = pd.DataFrame({
            'id': ['1', '2', '3'],
            'value': [10.5, 20.5, 30.5]
        })
        
        df['id'] = df['id'].astype(int)
        
        self.assertEqual(df['id'].dtype, int)


if __name__ == '__main__':
    unittest.main()
