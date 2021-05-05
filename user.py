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
    
    for doc in user_pref['hits']['hits']:
        #print("%s) %s" % (doc['_id'], doc['_source']['categories']))

        user_click = doc['_id'], doc['_source']['click']
        username = doc['_id'], doc['_source']['name']
        user_history = doc['_id'], doc['_source']['history']
    return user_history[1], user_click[1], username[1]