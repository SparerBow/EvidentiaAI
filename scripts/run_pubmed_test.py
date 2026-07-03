import os
import sys

# ensure workspace root is on sys.path so top-level packages are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.pubmed_agent import search_and_save


if __name__ == '__main__':
    query = 'covid vaccine'
    api_key = os.environ.get('NCBI_API_KEY')
    email = os.environ.get('NCBI_EMAIL')
    print(f"Searching and saving top 1 result for: {query} (api_key={'set' if api_key else 'not set'})")
    search_and_save(query, max_results=1, api_key=api_key, email=email)
