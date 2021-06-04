import os

from elasticsearch import Elasticsearch
from flask import Flask, render_template

app = Flask(__name__)

es = Elasticsearch(f"{os.environ['ES_HOST']}:{os.environ['ES_PORT']}", http_auth=('elastic', 'changeme'))

@app.route("/<user>")
def index(user):
    return render_template('hello.html', name=user)
