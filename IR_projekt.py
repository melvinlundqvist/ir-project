from elasticsearch import Elasticsearch, helpers
import os, sys
import json


# Setting up flask app and elasticsearch API connection
directory = '/Users/linn/Desktop/Search Engine'
es = Elasticsearch('127.0.0.1', port=9200)

def load_json(directory):
    " Use a generator, no need to load all in memory "
    for filename in os.listdir(directory):
        doc = []
        if filename.endswith('.json'):
            #with open('/Users/linn/Desktop/Search Engine/' + filename,'r') as open_file:
            #    yield json.load(open_file)

            for line in open('/Users/linn/Desktop/Search Engine/' + filename,'r'):
                doc.append(json.loads(line))
            yield doc
            #yield json.load(open('/Users/linn/Desktop/Search Engine/' + filename,'r'))

def search_results(query):
    res = es.search(index='articles', body={"query": {"match_all": {}}})
    return res['hits']

if __name__ == "__main__":
    helpers.bulk(es, load_json(directory), index='articles', doc_type='headline')
    query = input("Enter your query: ")
    print(search_results(query))