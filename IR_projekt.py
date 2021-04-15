from elasticsearch import Elasticsearch, helpers
import os, sys, uuid
import json

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

# Bulk indexing data
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

def search_results(keyword, index, field):
    res = es.search(
        index=index,
        body={
            "query":{
                "match": {
                    field: keyword
                }
            }
        }
    )
    return res

# Prints docID and article category
def format_results(results):
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("%s) %s" % (doc['_id'], doc['_source']['category']))

if __name__ == "__main__":
    directory = '/Users/linn/Desktop/'
    # Run elastic search locally
    es = Elasticsearch('127.0.0.1', port=9200, timeout=60)
    print("Elastic Running")
    # Create index
    helpers.bulk(es, bulk_json_data("../News_Category_Dataset_v2.json", "articles", "headline"), index ="articles")
    # Print results
    on = True # Enables querying multiple times
    while on == True:
        query = input("Enter your query: ")
        results = search_results(query, "articles", "headline")
        print(results)
        print(format_results(results))