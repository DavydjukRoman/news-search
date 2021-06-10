import os
import logging
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

app = Flask(__name__)

es = Elasticsearch(
    f"{os.environ['ES_HOST']}:{os.environ['ES_PORT']}",
    http_auth=('elastic', 'changeme')
)
print('ELASTIC INFO')
print(es)

logger = logging.getLogger('apppp')


@app.route("/")
def search():
    return render_template('search.html')


@app.route("/results", methods=['GET', 'POST'])
def search_request():
    search_term = request.form['input']
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
    logger.info("BODY")
    return render_template('results.html', res=res, total=res['hits']['total'])
