import os
from database import db


def test_create_tables_and_insert(tmp_path):
    db_file = tmp_path / "test_evidentia.db"
    db.DB_NAME = str(db_file)
    db.create_tables()
    # ensure tables exist by inserting a search history and a study
    db.insert_search_history('test query')
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
    assert row[1] == 'TEST123'
    history = db.list_search_history()
    assert len(history) >= 1
