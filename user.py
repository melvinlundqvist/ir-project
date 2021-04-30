from elasticsearch import Elasticsearch, helpers
import os, sys, uuid
import json

def user_preferences(es, user):
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
        username = doc['_id'], doc['_source']['name']
        #print(user_name)
    return user_pref[1][0], username[1]