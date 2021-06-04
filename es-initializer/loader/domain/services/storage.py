from typing import List
from abc import ABC, abstractmethod

from loader.domain.entities import News


class NewsStorage(ABC):
    @abstractmethod
    def store(self, news: List[News]):
        ...

    @abstractmethod
    def clean(self):
        ...
