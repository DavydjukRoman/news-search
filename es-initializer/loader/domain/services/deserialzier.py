from abc import ABC, abstractmethod

from loader.domain.entities import News


class NewsDeserializer(ABC):
    @abstractmethod
    def deserialize(self, row: str) -> News:
        ...
