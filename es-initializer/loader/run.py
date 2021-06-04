import os

from loader.domain.entities import News

from loader.infrastructure.serializers import DictNewsSerializer
from loader.infrastructure.deserialziers import JsonNewsDeserializer
from loader.infrastructure.sources import FilesNewsSource
from loader.infrastructure.storages import ElasticSearchNewsStorage
from loader.usecases.loader import load


if __name__ == "__main__":
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

from logging import getLogger


logger = getLogger("my logger")

logger.info("test")
logger.debug("test")
logger.exception(e)
logger.warning("hzz")
logger.critical("pizdec")
