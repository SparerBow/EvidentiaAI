import os
import pandas as pd
from typing import Tuple


UPLOAD_DIR = os.path.join('uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_excel(path: str) -> Tuple[bool, str]:
    """Basic validation for uploaded excel files. Returns (ok, message)."""
    try:
        df = pd.read_excel(path)
        if df.empty:
            return False, 'Empty spreadsheet'
        return True, f'OK ({len(df)} rows)'
    except Exception as e:
        return False, str(e)


def save_upload(file_obj, filename: str) -> str:
    target = os.path.join(UPLOAD_DIR, filename)
    with open(target, 'wb') as f:
        f.write(file_obj.getbuffer())
    return target
