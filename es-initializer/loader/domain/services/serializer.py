from abc import ABC, abstractmethod

from loader.domain.entities import News


class NewsSerializer(ABC):
    @abstractmethod
    def serialize(self, news: News):
        ...
