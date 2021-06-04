from typing import List

from elasticsearch import Elasticsearch, helpers

from loader.domain.entities import News
from loader.domain.services import NewsStorage

from loader.infrastructure.serializers import DictNewsSerializer


class ElasticSearchNewsStorage(NewsStorage):

    def __init__(self, es_host, es_port, es_user, es_pass, index: str, serializer: DictNewsSerializer):
        self.index = index
        self.es = Elasticsearch(f"{es_host}:{es_port}", http_auth=(es_user, es_pass))
        self.serializer = serializer

    def store(self, news: List[News]):
        helpers.bulk(
            client=self.es,
            actions=[
                {
                    '_op_type': 'index',
                    "_index": self.index,
                    "_source": self.serializer.serialize(new)
                } for new in news
            ]
        )

    def clean(self):
        # TODO can we delete all elements, not index
        self.es.indices.delete(index=self.index)
