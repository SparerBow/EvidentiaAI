"""Agent to orchestrate literature discovery: search PubMed and save to DB."""
import services.pubmed_service as ps
from database import db
from config.logger import get_logger
from config.settings import SETTINGS
from agents.base_agent import BaseAgent
from typing import List, Dict

logger = get_logger(__name__)


class LiteratureDiscoveryAgent(BaseAgent):
    def __init__(self):
        db.create_tables()

    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        logger.info('Searching PubMed: %s', query)
        ids = ps.search_pubmed(query, retmax=max_results, email=SETTINGS.PUBMED_EMAIL)
        if not ids:
            return []
        return ps.fetch_details(ids, email=SETTINGS.PUBMED_EMAIL)

    def save(self, items: List[Dict]):
        for s in items:
            try:
                db.insert_study(s)
            except Exception:
                logger.exception('Failed to insert study %s', s.get('pmid'))

    def search_and_save(self, query: str, max_results: int = 20) -> List[Dict]:
        items = self.search(query, max_results=max_results)
        if items:
            self.save(items)
            db.insert_search_history(query)
        return items


if __name__ == '__main__':
    agent = LiteratureDiscoveryAgent()
    res = agent.search_and_save('NSCLC pembrolizumab', max_results=5)
    print(f'Saved {len(res)} studies')


# backward-compatible function API
def search_and_save(query: str, max_results: int = 20):
    agent = LiteratureDiscoveryAgent()
    return agent.search_and_save(query, max_results=max_results)
