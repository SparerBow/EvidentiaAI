from config import settings


def test_settings_loads():
    # SETTINGS should be available even if .env is absent
    s = settings.SETTINGS
    assert hasattr(s, 'PUBMED_EMAIL')
    assert hasattr(s, 'OPENAI_API_KEY')
