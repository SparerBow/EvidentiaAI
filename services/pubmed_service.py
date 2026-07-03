"""PubMed service using BioPython Entrez to search and fetch records."""
from typing import List, Optional
import xml.etree.ElementTree as ET

from config.settings import SETTINGS


def _configure_entrez(email: Optional[str] = None, api_key: Optional[str] = None):
    # import Entrez lazily to avoid import-time dependency during tests
    from Bio import Entrez
    Entrez.email = email or SETTINGS.PUBMED_EMAIL
    if api_key:
        Entrez.api_key = api_key


def search_pubmed(query: str, retmax: int = 20, email: Optional[str] = None, api_key: Optional[str] = None) -> List[str]:
    _configure_entrez(email, api_key)
    from Bio import Entrez
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    record = Entrez.read(handle)
    handle.close()
    ids = record.get("IdList", [])
    return ids


def fetch_details(pmids: List[str], email: Optional[str] = None, api_key: Optional[str] = None) -> List[dict]:
    if not pmids:
        return []
    _configure_entrez(email, api_key)
    from Bio import Entrez
    ids = ",".join(pmids)
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    content = handle.read()
    handle.close()
    root = ET.fromstring(content)
    studies = []
    for article in root.findall('.//PubmedArticle'):
        pmid = article.findtext('.//PMID')
        title = article.findtext('.//ArticleTitle') or ""
        abstract_texts = [n.text or '' for n in article.findall('.//Abstract/AbstractText')]
        abstract = '\n'.join(abstract_texts).strip()
        journal = article.findtext('.//Journal/Title') or ""
        pub_year = article.findtext('.//Journal/JournalIssue/PubDate/Year')
        if not pub_year:
            medline = article.findtext('.//Journal/JournalIssue/PubDate/MedlineDate')
            pub_year = (medline or '')[:4]
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
    return studies


if __name__ == '__main__':
    # quick demo (requires PUBMED_EMAIL in env or config)
    ids = search_pubmed('NSCLC pembrolizumab', retmax=2)
    print(ids)
    print(fetch_details(ids))
