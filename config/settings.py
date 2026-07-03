from dataclasses import dataclass
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # allow operation without python-dotenv installed (tests/mock env)
    def load_dotenv():
        return None


@dataclass
class Settings:
    PUBMED_EMAIL: str = os.environ.get('PUBMED_EMAIL', '')
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')


SETTINGS = Settings()
