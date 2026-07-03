import os
import time
import logging
import requests
import xml.etree.ElementTree as ET
from typing import List, Optional

from database.db import create_tables, insert_study

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

logger = logging.getLogger(__name__)


def _build_eutils_params(api_key: Optional[str] = None, email: Optional[str] = None):
    params = {}
    if api_key:
        params["api_key"] = api_key
    if email:
        params["email"] = email
    # identify the tool to NCBI
    params.setdefault("tool", "EvdintiaAI")
    return params


def search_pubmed(query: str, retmax: int = 20, api_key: Optional[str] = None, email: Optional[str] = None) -> List[str]:
    url = EUTILS_BASE + "esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(retmax),
        "retmode": "json",
    }
    params.update(_build_eutils_params(api_key, email))
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    ids = data.get("esearchresult", {}).get("idlist", [])
    return ids


def fetch_details(pmids: List[str]) -> List[dict]:
    return fetch_details_with_auth(pmids, None, None)


def fetch_details_with_auth(pmids: List[str], api_key: Optional[str], email: Optional[str]) -> List[dict]:
    if not pmids:
        return []
    url = EUTILS_BASE + "efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    params.update(_build_eutils_params(api_key, email))
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    studies = []
    for article in root.findall('.//PubmedArticle'):
        try:
            pmid = article.findtext('.//PMID')
            title = article.findtext('.//ArticleTitle') or ""
            abstract_texts = [n.text or '' for n in article.findall('.//Abstract/AbstractText')]
            abstract = '\n'.join(abstract_texts).strip()
            journal = article.findtext('.//Journal/Title') or ""
            # publication year - try Year then MedlineDate
            pub_year = article.findtext('.//Journal/JournalIssue/PubDate/Year')
            if not pub_year:
                medline = article.findtext('.//Journal/JournalIssue/PubDate/MedlineDate')
                pub_year = (medline or '')[:4]
            # authors
            authors_list = []
            for a in article.findall('.//AuthorList/Author'):
                lastname = a.findtext('LastName')
                fore = a.findtext('ForeName')
                coll = a.findtext('CollectiveName')
                if coll:
                    authors_list.append(coll)
                elif lastname or fore:
                    authors_list.append(' '.join(filter(None, [fore, lastname])))
            authors = '; '.join(authors_list)

            studies.append({
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'journal': journal,
                'publication_year': pub_year,
                'authors': authors,
                'source': 'pubmed',
                'relevance_score': None,
            })
        except Exception:
            continue
    return studies


def search_and_save(query: str, max_results: int = 20, batch_size: int = 20, api_key: Optional[str] = None, email: Optional[str] = None):
    """Search PubMed for `query`, fetch details, and save to the local DB."""
    create_tables()
    # allow passing api_key/email or falling back to environment variables
    api_key = api_key or os.environ.get("NCBI_API_KEY")
    email = email or os.environ.get("NCBI_EMAIL")

    try:
        ids = search_pubmed(query, retmax=max_results, api_key=api_key, email=email)
    except requests.exceptions.RequestException as e:
        logger.error("Network error during PubMed search: %s", e)
        return

    if not ids:
        logger.info("No results found for query.")
        return

    try:
        studies = fetch_details_with_auth(ids, api_key, email)
    except requests.exceptions.RequestException as e:
        logger.error("Network error fetching PubMed details: %s", e)
        return

    for s in studies:
        insert_study(s)
        time.sleep(0.34)  # be kind to NCBI
    logger.info("Saved %d studies to the database.", len(studies))


if __name__ == '__main__':
    import sys

    q = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'cancer'
    print(f"Searching PubMed for: {q}")
    search_and_save(q, max_results=10)
