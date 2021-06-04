import json

from loader.domain.entities import News
from loader.domain.services import NewsSerializer


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
