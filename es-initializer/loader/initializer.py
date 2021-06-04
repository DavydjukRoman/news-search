# def load_json(path):
#     for file_name in listdir(path):
#         if file_name.endswith('.json'):
#             with open(file_name, 'r') as open_file:
#                 yield json.load(open_file)
#
# helpers.bulk(es, load_json('/news-search/existing-files/'), index='my-index', doc_type='my-type')
import ast
import os
import json
from datetime import datetime

from elasticsearch import Elasticsearch, helpers

print("Hello loader")


class News(object):
    def __init__(self, category: str, headline: str, authors: str,
                 link: str, short_description: str, date: str):
        self.category = category
        self.headline = headline
        self.authors = authors
        self.link = link
        self.short_description = short_description
        self.date = datetime.fromisoformat(date)

    def __str__(self):
        return self.headline

    def get_dict(self):
        return {
            'category': self.category,
            'headline': self.headline,
            'authors': self.authors,
            'link': self.link,
            'short_description': self.short_description,
            'date': self.date.isoformat(),
        }

    def get_json(self):
        return json.dumps({
            'category': self.category,
            'headline': self.headline,
            'authors': self.authors,
            'link': self.link,
            'short_description': self.short_description,
            'date': self.date.isoformat(),
        })


class FilesManager:
    def import_files(self, files_path: str, file_index: str):
        for file_name in os.listdir(files_path):
            if file_name.endswith('.json'):
                print('File name is:', file_name)
                self._import_json(f"{files_path}/{file_name}", file_index)
            # else:
            #     raise ValueError

    def _import_json(self, file_path, file_index):
        with open(file_path, 'r') as json_file:
            export_manager = ExportManager()
            export_manager.load_data_list(
                file_index=file_index,
                data_list=list(json_file.readlines())[:100]
            )


class ExportManager:
    def __init__(self):
        self.es = Elasticsearch(f"{os.environ['ES_HOST']}:{os.environ['ES_PORT']}",
                                http_auth=('elastic', 'changeme'))

    def load_data_list(self, file_index: str, data_list: list):
        helpers.bulk(
            client=self.es,
            actions=[
                {
                    '_op_type': 'index',
                    "_index": file_index,
                    "_source": News(**json.loads(row)).get_dict()
                } for row in data_list
            ]
        )


manager = FilesManager()
manager.import_files('data', 'news-set-test')
