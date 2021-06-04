import json

from loader.domain.entities import News
from loader.domain.services import NewsDeserializer


class JsonNewsDeserializer(NewsDeserializer):
    def deserialize(self, row: str) -> News:
        return News(**json.loads(row))
