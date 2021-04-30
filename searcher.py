from elasticsearch import Elasticsearch, helpers
import os, sys, uuid
import json

# Returns query results
def search_results(es, keyword, index, field):
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


# Prints docID and article category
def format_query(results):
    query_categories = []
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        query_categories.append(doc['_source']['category'])
    return query_categories
        #print("%s) %s" % (doc['_id'], doc['_source']['category']))
        #print("%s) %s" % (doc['_id'], doc['_score']))

# Update user preference based on search query & sort the results list
def format_results(user_history, user_pref, user_name, query_results):
    data = [doc for doc in query_results['hits']['hits']]
    results = {}
    combined_res = {}
    for history_list in user_history:
        combined_res = (combine_history(user_history))

    print(combined_res)
    print(len(combined_res))

    for doc in data:
        query_category = doc['_source']['category']
        headline = doc['_source']['headline']  
        doc_score = doc['_score']    
        total_score = 0.8*doc['_score'] + 0.2*user_pref.get(query_category)
        # Call combine_results document score with user_pref

        results[headline] = [total_score, query_category]
    results = sorted(results.items(), key=lambda item:item[1][0], reverse=True)
            #print("doc score: %s - user category score: %s total score: %s" % (doc_score, user_pref.get(query_category), total_score))
    print(results)
    return results

#Function to set score for categories in user_history
def combine_history(user_history):
    category_scores = {}
    for category in user_history:
        if category in category_scores:
            category_scores[category] += 1
        else:
            category_scores[category] = 1
    return category_scores

        

# Print short description for the article the user wants to read
def read_short_description(query_results, docID):
    data = [doc for doc in query_results['hits']['hits']]
    #for doc in data:
        #if doc['_id'] == docID:
            
            #print(doc['_source']['short_description'])

# Format user preferences in Users.json based on query results
def format_preferences_search(user_history, user_pref, username, results):
    i = 1 
    for score in results:
        query_category = score[1][1]
        with open("Users.json", "r") as jsonFile:
            users = json.load(jsonFile)
            for user in users:
                if user['name'] == username:
                    # Update user pref
                    #current_score = user['categories'][0][query_category]
                    #user['categories'][0][query_category] = update_user_pref(current_score)
                    #user['categories'][0][query_category] *= 1.02
                    if len(user['history']) <= 11:
                        user['history'].append(query_category)
                    else:
                        for j in range(5):
                            user['history'].pop(0)
                            print(user['history'])
                    break
        # Update user file
        with open("Users.json", "w") as jsonFile:
            json.dump(users, jsonFile)
            jsonFile.close()
        if i == 5:
            break
        i += 1


#def update_user_pref(current_score, ):
    

# Format user preferences in Users.json based on article selection
def format_preferences_click(username, docID):
    # get category for article
    data = [doc for doc in query_results['hits']['hits']]
    for doc in data:
        if doc['_id'] == docID:
            category = doc['_source']['category']
    # read user file
    with open("Users.json", "r") as jsonFile:
        users = json.load(jsonFile)
        for user in users:
            if user['name'] == username:
                user['categories'][0][category] += 1
                break
    # update user file
    with open("Users.json", "w") as jsonFile:
        json.dump(users, jsonFile)
        jsonFile.close()


