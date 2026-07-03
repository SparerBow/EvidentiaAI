from database.models import Study, SearchHistory


def test_models_dataclasses():
    s = Study(pmid='1', title='T')
    assert s.pmid == '1'
    h = SearchHistory(query='q')
    assert h.query == 'q'
