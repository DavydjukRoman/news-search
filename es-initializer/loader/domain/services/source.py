from abc import ABC, abstractmethod
from typing import List

from loader.domain.entities import News


class NewsSource(ABC):
    @abstractmethod
    def read(self) -> List[News]:
        ...
