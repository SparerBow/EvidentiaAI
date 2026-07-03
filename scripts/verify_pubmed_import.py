import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import services.pubmed_agent as pa
    print('import_ok')
except Exception as e:
    print('import_failed', e)
