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

# Get user preferences
def get_user_pref(user_name):
    with open("Users.json", "r") as jsonFile:
        users = json.load(jsonFile)
        for user in users:
            if user['name'] == user_name:
                return user.get("history"), user.get("click")

# Update results based on user preferences
def format_results(user_history, user_click, query_results, personalize, weights):
    results = []
    if personalize:
        combined_res_query = (combine_history(user_history))
        combined_click = combine_history(user_click)
        for doc in query_results['hits']['hits']:
            category = doc['_source']['category']
            doc_score = doc['_score']

            history_score = combined_res_query.get(category)
            click_score = combined_click.get(category)
            total_score = weights[0]*(doc_score / query_results['hits']['max_score'])
            #print("ES relevance score: " + str(total_score))

            if history_score is not None:
                total_score += weights[1]*(history_score / len(user_history))
                #print("History score: " + str(0.2*(history_score / len(user_history))))
            if click_score is not None:
                total_score += weights[2]*(click_score / len(user_click))
                #print("Click score: " + str(0.3*(click_score / len(user_click))))

            results.append({'score': total_score, 'category': category, 'headline': doc['_source']['headline'], 'short_description': doc['_source']['short_description']})
        results.sort(key=lambda item:item.get("score"), reverse=True)
    else:
        for doc in query_results['hits']['hits']:
            results.append({'score': doc['_score'], 'category': doc['_source']['category'], 'headline': doc['_source']['headline'], 'short_description': doc['_source']['short_description']})

    print("SEARCH RESULTS:\n")
    for i in range(len(results)):
        short_des = results[i].get('short_description')
        if short_des != "":
            print('%d. %s\n%s\n'% (i+1, results[i].get('headline'), short_des))
        else:
            print('%d. %s\nHas no short description...\n'% (i+1, results[i].get('headline')))
    return results

# Function to count appearences of categories in list
def combine_history(category_list):
    category_scores = {}
    for category in category_list:
        if category in category_scores:
            category_scores[category] += 1
        else:
            category_scores[category] = 1
    return category_scores

# Format user preferences in Users.json based on query results
def format_preferences_search(user_query, user_name, results):
    n = 5
    if len(results) < 5:
        n = len(results)
    for i in range(n):
        # read user file
        query_category = results[i].get("category")
        with open("Users.json", "r") as jsonFile:
            users = json.load(jsonFile)
            for user in users:
                if user['name'] == user_name:
                    user['history'].append(query_category)
                    if len(user['history']) > 10:
                        user['history'].pop(0)

        # update user file
        with open("Users.json", "w") as jsonFile:
            json.dump(users, jsonFile)
            jsonFile.close()

# Format user preferences in Users.json based on article selection
def format_preferences_click(user_name, category):
    # read user file
    with open("Users.json", "r") as jsonFile:
        users = json.load(jsonFile)
        for user in users:
            if user['name'] == user_name:
                user['click'].append(category)
                if len(user['click']) > 5:
                    user['click'].pop(0)

    # update user file
    with open("Users.json", "w") as jsonFile:
        json.dump(users, jsonFile)
        jsonFile.close()


