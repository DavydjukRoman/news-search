from typing import List
from loader.domain.entities import News
from loader.domain.services import NewsSource


class PostgresNewsSource(NewsSource):

    def read(self) -> List[News]:
        # ToDo: learn postgre
        ...
