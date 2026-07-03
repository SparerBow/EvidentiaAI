import os
from database import db


def test_insert_and_get(tmp_path):
    db_file = tmp_path / "test.db"
    # direct-path assignment to use isolated DB for tests
    db.DB_NAME = str(db_file)
    db.create_tables()
    s = {
        'pmid': 'TEST123',
        'title': 'T',
        'abstract': 'A',
        'journal': 'J',
        'publication_year': '2020',
        'authors': 'X',
        'source': 'pubmed',
        'relevance_score': 0.5,
    }
    db.insert_study(s)
    row = db.get_study_by_pmid('TEST123')
    assert row is not None
    # schema: (study_id, pmid, title, abstract, journal, publication_year, authors, source, relevance_score)
    assert row[1] == 'TEST123'
    assert row[2] == 'T'
