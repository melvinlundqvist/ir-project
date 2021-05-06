from elasticsearch import Elasticsearch, helpers
import os, sys, uuid
import json
import tkinter as tk
import user
import searcher
import indexer

personalize = None
user = ""
results = []
weights = [0.5, 0.2, 0.3]

# perform the search
def click_search():
    input_text = entry.get()
    if input_text:
        entry.delete(0, 'end')
        lbl_message.config(text="\n\n")
        listbox.delete(0, 'end')
        textbox.delete('1.0', 'end')

        # get user preferences
        user_history, user_click = searcher.get_user_pref(user)

        # get query results
        query_results = searcher.search_results(es, input_text, "articles", "headline")

        # rearrange results based on users preference
        global results
        results = searcher.format_results(user_history, user_click, query_results, personalize, weights)

        # update gui with results
        n_hits = query_results['hits']['total']['value']
        message = 'Got %d hits in %.3f seconds.' % (n_hits, query_results['took'] / 1000)
        if n_hits > 10:
            message += " The first ten hits are:"
        lbl_message.config(text="\n" + message + "\n")
        for i in range(len(results)):
            line = '%d. %s - %.3f' % (i+1, results[i].get('headline'), results[i].get('score'))
            listbox.insert('end', line)

        # update user preferences in Users.json based on results
        searcher.format_preferences_search(user_history, user, results)

def click_article(event):
    textbox.delete('1.0', 'end')
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        item = event.widget.get(index)
        res_object = results[int(item[0])-1]
        textbox.insert('end', res_object.get('short_description'))
        searcher.format_preferences_click(user, res_object.get('category'))

# verify user name
def click_start():
    input_text = entry.get()
    with open("Users.json", "r") as jsonFile:
        users = json.load(jsonFile)
        for user_object in users:
            if user_object['name'] == input_text:
                global user
                user = input_text
                lbl_input.config(text="Search query")
                entry.delete(0, 'end')
                btn.config(text="Search", command=click_search)
                lbl_message.config(text="\nWelcome " + input_text + "!\n")
                listbox.pack(fill='both')
                listbox.bind("<<ListboxSelect>>", click_article)
                lbl_short_d.pack()
                textbox.pack(fill='x')
                if personalize:
                    lbl_settings.pack()
                    frame_lbls.pack(side='left')
                    frame_entries.pack(side='left')
                    btn_save.pack(side='left')
                return
    lbl_message.config(text="\nIncorrect username.")

def update_weights():
    entry_r_score.delete(0, 'end')
    entry_r_score.insert(0, '%.2f' % weights[0])
    entry_history.delete(0, 'end')
    entry_history.insert(0, '%.2f' % weights[1])
    entry_click.delete(0, 'end')
    entry_click.insert(0, '%.2f' % weights[2])

# save weight settings
def click_save():
    w1 = float(entry_r_score.get())
    w2 = float(entry_history.get())
    w3 = float(entry_click.get())
    sum = w1 + w2 + w3
    global weights
    weights = [w1/sum, w2/sum, w3/sum]
    update_weights()

# initiate gui window
window = tk.Tk()
window.title('Personalized Search Engine')
window.geometry('500x600')
window.configure(bg='black')

lbl_input = tk.Label(window, text="User Name", bg="black", fg="white", font="none 12 bold")
lbl_input.pack()
entry = tk.Entry(window, bg="white", fg="black", insertbackground="black")
entry.pack()
btn = tk.Button(window, text="Submit", bd=0, bg="blue", fg="black", font="none 12 bold", command=click_start)
btn.pack()
lbl_message = tk.Label(window, text="", bg="black", fg="white", font="none 12")
lbl_message.pack()
listbox = tk.Listbox(window)
lbl_short_d = tk.Label(window, text="\nIf you open an article you can read a short description here (if it has one):\n", bg="black", fg="white", font="none 12")
textbox = tk.Text(window, height=6)
lbl_settings = tk.Label(window, text="\nWeight settings:", bg="black", fg="white", font="none 12 bold")
frame_lbls = tk.Frame(window, bg="black")
lbl_r_score = tk.Label(frame_lbls, text="Relevance score", pady=5, bg="black", fg="white", font="none 12 bold").pack()
lbl_history = tk.Label(frame_lbls, text="Search history", pady=5, bg="black", fg="white", font="none 12 bold").pack()
lbl_click = tk.Label(frame_lbls, text="Click history", pady=5, bg="black", fg="white", font="none 12 bold").pack()
frame_entries = tk.Frame(window, bg="black")
entry_r_score = tk.Entry(frame_entries, bd=0, width=4, bg="white", fg="black", insertbackground="black")
entry_r_score.pack()
entry_history = tk.Entry(frame_entries, bd=0, width=4, bg="white", fg="black", insertbackground="black")
entry_history.pack()
entry_click = tk.Entry(frame_entries, bd=0, width=4, bg="white", fg="black", insertbackground="black")
entry_click.pack()
update_weights()
btn_save = tk.Button(window, text="Normalize and save", bd=0, bg="blue", fg="black", font="none 12 bold", command=click_save)


if __name__ == "__main__":
    # arguments should be 'do indexing' and 'personalize', both True or False (not case sensitive)
    args = sys.argv[1:]
    if len(args) != 2:
        print("Missing argument(s)! Provide whether you want do indexing and personalization.")
        sys.exit(1)
    if args[0].lower() == 'true':
        do_indexing = True
    elif args[0].lower() == 'false':
        do_indexing = False
    else:
        print("The first argument you provided wasn't 'True' or 'False'")
        sys.exit(1)
    if args[1].lower() == 'true':
        personalize = True
    elif args[1].lower() == 'false':
        personalize = False
    else:
        print("The second argument you provided wasn't 'True' or 'False'")
        sys.exit(1)

    # run elastic search locally
    es = Elasticsearch('127.0.0.1', port=9200, timeout=60)
    print("Elastic Running!")

    # create article index  
    if do_indexing:
        helpers.bulk(es, indexer.bulk_json_data("../News_Category_Dataset_v2.json", "articles", "headline"), index ="articles")

    window.mainloop()