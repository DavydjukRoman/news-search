from typing import Dict

from loader.domain.entities import News
from loader.domain.services import NewsSerializer


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
