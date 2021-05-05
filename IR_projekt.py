from elasticsearch import Elasticsearch, helpers
import os, sys, uuid
import json

import user as user
import searcher as searcher
import indexer as indexer

# Run elastic search locally
es = Elasticsearch('127.0.0.1', port=9200, timeout=60)
print("Elastic Running")

# Create article index
#helpers.bulk(es, indexer.bulk_json_data("../News_Category_Dataset_v2.json", "articles", "headline"), index ="articles")

# Create user index
indexer.load_users_json(es)

# Get user preferences (categories)
user_name = input("Enter user name: ")

while True:
    user_history, user_click, username = searcher.get_user_pref(user_name)
    # Get query results
    query = input("Enter your query: ")
    query_results = searcher.search_results(es, query, "articles", "headline")

    # Modify search results
    # Format results rearranges results according to users preference
    results = searcher.format_results(user_history, user_click, username, query_results)
    # Format user preferences adds score to categories in user.json
    searcher.format_preferences_search(user_history, username, results)

    # user clicks on an article (will be done in interface later)
    ID = input("Enter ID of the article you want to read: ")
    searcher.read_short_description(results, query_results, ID)
    searcher.format_preferences_click(results, user_name, ID)

# Modify user preferences (Top 5 search results) 
# Scores are calculated based on categories in query results

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