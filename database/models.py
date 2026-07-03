from dataclasses import dataclass
from typing import Optional


@dataclass
class Study:
    pmid: str
    title: str
    abstract: Optional[str] = None
    journal: Optional[str] = None
    publication_year: Optional[str] = None
    authors: Optional[str] = None
    source: Optional[str] = 'pubmed'
    relevance_score: Optional[float] = None


@dataclass
class SearchHistory:
    query: str
    searched_at: Optional[str] = None
