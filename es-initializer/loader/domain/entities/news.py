from datetime import datetime
from dataclasses import dataclass


@dataclass()
class News:
    category: str
    headline: str
    authors:  str
    link:     str
    short_description: str
    date:     datetime
