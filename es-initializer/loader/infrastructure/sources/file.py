from typing import List

from loader.domain.entities import News
from loader.domain.services import NewsDeserializer, NewsSource


class FilesNewsSource(NewsSource):
    def __init__(self, path: str, deserializer: NewsDeserializer):
        self.path = path
        self.deserializer = deserializer

    def read(self) -> List[News]:
        with open(self.path, 'r') as json_file:
            return [self.deserializer.deserialize(row) for row in json_file.readlines()]
