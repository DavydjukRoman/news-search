# def load_json(path):
#     for file_name in listdir(path):
#         if file_name.endswith('.json'):
#             with open(file_name, 'r') as open_file:
#                 yield json.load(open_file)
#
# helpers.bulk(es, load_json('/news-search/existing-files/'), index='my-index', doc_type='my-type')
import os
import json
from datetime import datetime
from typing import List, Dict
from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch, helpers

from dataclasses import dataclass


@dataclass()
class News(object):
    category: str
    headline: str
    authors:  str
    link:     str
    short_description: str
    date:     datetime


class NewsSource(ABC):
    @abstractmethod
    def read(self) -> List[News]:
        ...


class NewsStorage(ABC):
    @abstractmethod
    def store(self, news: List[News]):
        ...

    @abstractmethod
    def clean(self):
        ...


class NewsDeserializer(ABC):
    @abstractmethod
    def deserialize(self, row: str) -> News:
        ...


class NewsSerializer(ABC):
    @abstractmethod
    def serialize(self, news: News):
        ...


class DictNewsSerializer(NewsSerializer):
    def serialize(self, news: News) -> Dict[str, str]:
        return {
            'category': news.category,
            'headline': news.headline,
            'authors': news.authors,
            'link': news.link,
            'short_description': news.short_description,
            'date': news.date.isoformat(),
        }


class JsonNewsSerializer(NewsSerializer):
    def serialize(self, news: News) -> str:
        return json.dumps({
            'category': news.category,
            'headline': news.headline,
            'authors': news.authors,
            'link': news.link,
            'short_description': news.short_description,
            'date': news.date.isoformat(),
        })


class FilesNewsSource(NewsSource):
    def __init__(self, path: str, deserializer: NewsDeserializer):
        self.path = path
        self.deserializer = deserializer

    def read(self) -> List[News]:
        with open(self.path, 'r') as json_file:
            return [self.deserializer.deserialize(row) for row in json_file.readlines()]


class JsonNewsDeserializer(NewsDeserializer):
    def deserialize(self, row: str) -> News:
        return News(**json.loads(row))


class PostgresNewsSource(NewsSource):

    def read(self) -> List[News]:
        # ToDo: learn postgre
        ...


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


def load(source: NewsSource, storage: NewsStorage):
    news: List[News] = source.read()
    storage.store(news)


load(
    FilesNewsSource(
        'data/News_Category_Dataset_v2.json',
        JsonNewsDeserializer()),
    ElasticSearchNewsStorage(
        es_host=os.environ['ES_HOST'],
        es_port=os.environ['ES_PORT'],
        es_user='elastic',
        es_pass='changeme',
        index='news-set-test-v2',
        serializer=DictNewsSerializer()
    )

)
