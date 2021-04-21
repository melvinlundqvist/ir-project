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

def load_users_json():
    " Use a generator, no need to load all in memory"
    f = open('Users.json')
    data = json.load(f)
    for i in data:
        res = es.index(index='users',doc_type='user_data',body=i)

# Bulk indexing data
def bulk_json_data_boosted(json_file, _index, doc_type):
    print("Indexing...")
    yield {
        "mappings": {
            "properties": {
                "_source": {
                    "category": "rank_features"
                }
            }
        }
    }
    json_list = get_data_from_file(json_file)
    for doc in json_list:
        doc = json.loads(doc)
        # use a 'yield' generator so that the data
        # isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                #"_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": {
                    "category": {
                        doc.category: 1
                    },
                    "headline": doc.headline,
                    "authors": doc.authors,
                    "link": doc.link,
                    "short_description": doc.short_description,
                    "date":doc.date,
                }
            }

def search_results_boosted(keyword, index, field):
    res = es.search(
        index=index,
        body={
            "query":{
                "bool": {
                    "must": [
                        {
                            "match": {
                                field: keyword
                            }
                        }
                    ],
                    "should": [
                        {
                            "rank_feature": {
                                "field": "_source.COMEDY",
                                "boost": 1
                            }
                        }
                    ]
                }
            }
        }
    )
    return res

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
    #query_categories = format_query(res)
    #return query_categories

#Function to combine personalized preferences with search results
#def combine_results():
    

# Prints docID and article category
def format_query(results):
    query_categories = []
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        query_categories.append(doc['_source']['category'])
    return query_categories
        #print("%s) %s" % (doc['_id'], doc['_source']['category']))
        #print("%s) %s" % (doc['_id'], doc['_score']))

#Personalizes the search results based on user preferences and query results
def format_results(preferences, query_results):
    #print(query_results)
    data = [doc for doc in query_results['hits']['hits']]
    for c in preferences:
        if preferences.get(c) > 0:
            for doc in data:
                query_category = doc['_source']['category']
                if query_category in c:
                    print("Categories in user pref which matches query category: " + str(c))
                else:
                    print("No categories match")
            #print(user_pref[1][0].get(c))
           
# Format user preferences in Users.json based on search results
#def format_preferences(preferences, results)

def user_preferences(user):
    user_pref = es.search(
        index="users",
        body={
            "query":{
                "match": {
                    "name": user
                }
            }
        }
    )

    data = [doc for doc in user_pref['hits']['hits']]
    
    for doc in data:
        #print("%s) %s" % (doc['_id'], doc['_source']['categories']))
        
        # user_pref[1][0] is a dictonary where key = category, value = score
        user_pref = doc['_id'], doc['_source']['categories']
        return user_pref[1][0]

if __name__ == "__main__":
    directory = '/Users/linn/Desktop/'
    # Run elastic search locally
    es = Elasticsearch('127.0.0.1', port=9200, timeout=60)
    print("Elastic Running")
    
    # Create article index
    #helpers.bulk(es, bulk_json_data("../News_Category_Dataset_v2.json", "articles", "headline"), index ="articles")

    # Create user index
    load_users_json()

    # Get user preferences (categories)
    user = input("Enter user name: ")
    user_pref = user_preferences(user)
    
    # Get query results
    query = input("Enter your query: ")
    query_results = search_results(query, "articles", "headline")
    
    # Modify search results
    # Format results rearranges results according to users preference
    format_results(user_pref, query_results)
    #format_pref = format_preferences(user_pref, results)

    # Modify user preferences (Top 5 search results) 
    # Format user preferences adds score to categories in user.json
    # Scores are calculated based on categories in query results
    # format_preferences(user_pref, query_results)

    # Print results
    #on = True # Enables querying multiple times
    #while on == True:
    #    query = input("Enter your query: ")
    #    results = search_results(query, "articles", "headline")
        #results_boosted = search_results_boosted(query, "articles", "headline")
        #for res in results:
        #    print(results)
        #print("Boosted Results: " + str(format_results(results_boosted)))
        #print("Results: " + str(format_results(results)))