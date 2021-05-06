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

def get_user_pref(user_name):
    with open("Users.json", "r") as jsonFile:
        users = json.load(jsonFile)
        for user in users:
            if user['name'] == user_name:
                return user.get("history"), user.get("click"), user.get("name")

# Update user preference based on search query & sort the results list
def format_results(user_query, user_click, user_name, query_results):
    results = []
    combined_res_query = (combine_history(user_query))
    combined_click = combine_history(user_click)

    #print(combined_res_query)
    #print(len(combined_res_query))
    doc_scores = []
    for doc in query_results['hits']['hits']:
        doc_scores.append(doc['_score'])

    i = 1
    for doc in query_results['hits']['hits']:
        query_category = doc['_source']['category']
        headline = doc['_source']['headline']  
        doc_score = doc['_score']
        doc_id = doc['_id']
        print(str(i) + " - " + str({"score": doc_score, "category": query_category, "headline": headline}))
        i += 1
        history_score = combined_res_query.get(query_category)
        click_score = combined_click.get(query_category)
        total_score = 0.5*(doc_score / max(doc_scores))
        print("total " + str(total_score))
        if history_score is not None:
            total_score += 0.2*(history_score / len(user_query))
            #print("len user_query " + str(len(user_query)))
            print("history " + str(0.2*(history_score / len(user_query))))
        if click_score is not None:
            total_score += 0.3*(click_score / len(user_click))
            print("click " + str(0.3*(click_score / len(user_click))))
        results.append({"score": total_score, "category": query_category, "headline": headline})

    results.sort(key=lambda item:item.get("score"), reverse=True)

    print("SEARCH RESULTS:")
    for i in range(len(results)):
        print(str(i+1) + " - " + str(results[i]))
    return results

#Function to set score for categories in user_query
def combine_history(category_list):
    category_scores = {}
    for category in category_list:
        if category in category_scores:
            category_scores[category] += 1
        else:
            category_scores[category] = 1
    return category_scores

# Print short description for the article the user wants to read
def read_short_description(results, query_results, ID):
    docID = results[int(ID)-1].get("id")
    for doc in query_results['hits']['hits']:
        if doc['_id'] == docID:
            print(doc['_source']['short_description'])

# Format user preferences in Users.json based on query results
def format_preferences_search(user_query, username, results):
    for i in range(5):
        query_category = results[i].get("category")
        with open("Users.json", "r") as jsonFile:
            users = json.load(jsonFile)
            for user in users:
                if user['name'] == username:
                    user['history'].append(query_category)
                    if len(user['history']) > 10:
                        user['history'].pop(0)
        # Update user file
        with open("Users.json", "w") as jsonFile:
            json.dump(users, jsonFile)
            jsonFile.close()

#def update_user_click(current_score, ):  

# Format user preferences in Users.json based on article selection
def format_preferences_click(results, username, ID):
    # get category for article
    category = results[int(ID)-1].get("category")
    print(category)
    # read user file
    with open("Users.json", "r") as jsonFile:
        users = json.load(jsonFile)
        for user in users:
            if user['name'] == username:
                print(category)
                user['click'].append(category)
                if len(user['click']) > 5:
                    user['click'].pop(0)
    # update user file
    with open("Users.json", "w") as jsonFile:
        json.dump(users, jsonFile)
        jsonFile.close()


