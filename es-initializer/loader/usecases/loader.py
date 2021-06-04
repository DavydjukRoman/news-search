from typing import List

from loader.domain.entities import News
from loader.domain.services import NewsSource, NewsStorage


def load(source: NewsSource, storage: NewsStorage):
    news: List[News] = source.read()
    storage.store(news)
