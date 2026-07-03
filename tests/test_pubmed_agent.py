import os

import database.db as db
import agents.literature_discovery_agent as pa
import services.pubmed_service as ps


def test_search_and_save(monkeypatch, tmp_path):
    # use an isolated DB
    db_file = tmp_path / "pubmed.db"
    db.DB_NAME = str(db_file)

    # patch service functions to avoid network/BioPython dependency
    monkeypatch.setattr(ps, 'search_pubmed', lambda query, retmax=1, email=None: ['111'])

    def fake_fetch(ids, email=None):
        return [{
            'pmid': '111',
            'title': 'Sample Title',
            'abstract': 'Sample abstract',
            'journal': 'Journal X',
            'publication_year': '2021',
            'authors': 'John Doe',
            'source': 'pubmed',
            'relevance_score': None,
        }]

    monkeypatch.setattr(ps, 'fetch_details', fake_fetch)

    pa.search_and_save('test query', max_results=1)

    rows = db.list_studies()
    assert len(rows) == 1
    row = rows[0]
    assert row[1] == '111'
    assert 'Sample Title' in row[2]
