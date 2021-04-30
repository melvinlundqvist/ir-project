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
#helpers.bulk(es, bulk_json_data("../News_Category_Dataset_v2.json", "articles", "headline"), index ="articles")

# Create user index
indexer.load_users_json(es)

# Get user preferences (categories)
user_input = input("Enter user name: ")
user_history, user_pref, username = user.user_preferences(es, user_input)

# Get query results
query = input("Enter your query: ")
query_results = searcher.search_results(es, query, "articles", "headline")

# Modify search results
# Format results rearranges results according to users preference
results = searcher.format_results(user_history, user_pref, username, query_results)
# Format user preferences adds score to categories in user.json
searcher.format_preferences_search(user_history, user_pref, username, results)
# user clicks on an article (will be done in interface later)

#docID = input("Enter ID of the article you want to read: ")
#searcher.read_short_description(query_results, docID)


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