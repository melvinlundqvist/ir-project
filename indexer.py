from elasticsearch import Elasticsearch, helpers
import os, sys, uuid
import json

def run_elastic():
    es = Elasticsearch('127.0.0.1', port=9200, timeout=60)
    print("Elastic Running")

def script_path():
    path = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix': # macOS/Linux
        path = path + "/"
    else:
        path = path + chr(92) # Windows
    return path

def get_data_from_file(self, path=script_path()):
    file = open(path + str(self), encoding="utf8", errors='ignore')
    data = [line.strip() for line in file]
    file.close()
    return data

# Bulk index articles
def bulk_json_data(json_file, _index, doc_type):
    print("Indexing...")
    json_list = get_data_from_file(json_file)
    for doc in json_list:
        # use a 'yield' generator so that the data
        # isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                #"_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }           
# Index users
def load_users_json(es):
    " Use a generator, no need to load all in memory"
    f = open('Users.json')
    data = json.load(f)
    for i in data:
        res = es.index(index='users',doc_type='user_data',body=i)
