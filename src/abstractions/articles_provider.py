from abc import ABC, abstractmethod
from typing import Optional

class ArticlesProvider(ABC):
    @abstractmethod
    def get_async(self, paths: list[str]) -> tuple[Optional[str], str]:
        pass
