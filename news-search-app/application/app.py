import os
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List
import logging
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

app = Flask(__name__)

es = Elasticsearch(
    f"{os.environ['ES_HOST']}:{os.environ['ES_PORT']}",
    http_auth=('elastic', 'changeme')
)
print('ELASTIC INFO')
print('ELASTIC INFO')
print('ELASTIC INFO')
print(es)

logger = logging.getLogger('apppp')

@app.route("/")
def home():
    return str(es)


@app.route("/<user>")
def user(user):
    return render_template('hello.html', name=user)


@app.route("/search")
def search():
    return render_template('search.html')


@app.route("/search/results", methods=['GET', 'POST'])
def search_request():
    print("56756756")
    search_term = request.form['input']
    # res = es.search(
    #     index='news-set-test.index',
    #     size=5,
    #     body={
    #         'query': {
    #             "multi_match": {
    #                 "query": search_term
    #             }
    #         }
    #     }
    # )
    res = es.search(
        index='news-set-test',
        body={
            'track_total_hits': True,
            'query': {
                'multi_match': {
                    "query": search_term
                }
            }

        }
    )
    logger.info("BODY BODY BODY")
    print(search_term)
    print(res['hits']['hits'])
    return render_template('results.html', res=res)

# @dataclass()
# class News:
#     category: str
#     headline: str
#     authors: str
#     link: str
#     short_description: str
#     date: datetime
#
#
# class NewsExtractor(ABC):
#     @abstractmethod
#     def get_news_by_category(self, news_category: str) -> List[News]: ...
#     # def get_headlines(self):...
#     # def get_authors(self):...
#     # def get_links(self):...
#     # def get_short_description(self):
#
#
# class ElasticNewsExtractor(NewsExtractor):
#     def __init__(self, index: str):
#         self.index = index
#
#     def get_news_by_category(self, news_category: str) -> List[News]:
#         pass
#
#
# news_extractor = ElasticNewsExtractor(
#     index='news-set-test'
# )
#
# category = 'COMEDY'
# print(news_extractor.get_news_by_category(category))
