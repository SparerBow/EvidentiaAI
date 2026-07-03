import os
from types import SimpleNamespace

import database.db as db
import services.pubmed_agent as pa


def make_resp_json(obj):
    r = SimpleNamespace()
    r.status_code = 200
    r.json = lambda: obj
    r.raise_for_status = lambda: None
    return r


def make_resp_content(xmlstr):
    r = SimpleNamespace()
    r.status_code = 200
    r.content = xmlstr.encode('utf-8')
    r.raise_for_status = lambda: None
    return r


def fake_get(url, params=None, timeout=None):
    if 'esearch.fcgi' in url:
        return make_resp_json({"esearchresult": {"idlist": ["111"]}})
    if 'efetch.fcgi' in url:
        xml = """<?xml version="1.0"?>
        <PubmedArticleSet>
          <PubmedArticle>
            <MedlineCitation>
              <PMID>111</PMID>
              <Article>
                <ArticleTitle>Sample Title</ArticleTitle>
                <Abstract><AbstractText>Sample abstract</AbstractText></Abstract>
                <Journal>
                  <Title>Journal X</Title>
                  <JournalIssue><PubDate><Year>2021</Year></PubDate></JournalIssue>
                </Journal>
                <AuthorList>
                  <Author><LastName>Doe</LastName><ForeName>John</ForeName></Author>
                </AuthorList>
              </Article>
            </MedlineCitation>
          </PubmedArticle>
        </PubmedArticleSet>
        """
        return make_resp_content(xml)
    raise RuntimeError("unexpected URL")


def test_search_and_save(monkeypatch, tmp_path):
    # patch requests.get to avoid network
    import requests

    monkeypatch.setattr(requests, 'get', fake_get)

    # use an isolated DB
    db_file = tmp_path / "pubmed.db"
    db.DB_NAME = str(db_file)

    pa.search_and_save('test query', max_results=1)

    rows = db.list_studies()
    assert len(rows) == 1
    row = rows[0]
    assert row[1] == '111'
    assert 'Sample Title' in row[2]
