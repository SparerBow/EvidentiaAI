import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import services.pubmed_agent as pa
import scripts.cli as cli


def test_cli_invokes_search_and_save(monkeypatch):
    called = {}

    def fake_search_and_save(query, max_results=10, batch_size=20, api_key=None, email=None):
        called['args'] = (query, max_results, api_key, email)

    # monkeypatch the function actually referenced by the CLI module
    monkeypatch.setattr(cli, 'search_and_save', fake_search_and_save)

    cli.main(['--query', 'abc', '--max', '3', '--api-key', 'KEY', '--email', 'e@x'])

    assert called['args'][0] == 'abc'
    assert called['args'][1] == 3
    assert called['args'][2] == 'KEY'
    assert called['args'][3] == 'e@x'
