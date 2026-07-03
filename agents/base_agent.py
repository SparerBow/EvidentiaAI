from abc import ABC, abstractmethod
from typing import List, Dict


class BaseAgent(ABC):
    """Abstract base agent for literature/evidence agents."""

    @abstractmethod
    def search(self, query: str, **kwargs) -> List[Dict]:
        """Search for items matching `query` and return structured results."""

    @abstractmethod
    def save(self, items: List[Dict]):
        """Persist a list of structured items to storage."""

    def search_and_save(self, query: str, **kwargs):
        items = self.search(query, **kwargs)
        self.save(items)
        return items
