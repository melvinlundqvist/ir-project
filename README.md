# Personalized Search
Repository for project in the course Search Engines and Information Retrieval Systems at KTH.

### Installation
1. You will need to install the `elasticsearch` package. There are several ways to do this but for example with pip:
```
$ python -m pip install elasticsearch
```
or with Homebrew:
```
$ brew install elastic/tap/elasticsearch-full
```
You can find more info on how to install Elasticsearch [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html).

2. You will also need to clone this repository to run the GUI locally. This can be done with SSH like this:
```
$ git clone git@github.com:melvinlundqvist/ir-project.git
```

3. You will need to download the dataset with articles. This can be done from Kaggle [here](https://www.kaggle.com/rmisra/news-category-dataset).
The dataset is a JSON-file which you should place in the folder outside this cloned repository folder.

### Run
1. First, you'll need to start Elasticsearch so open a command line and run:
```
$ bin/elasticsearch
```
More on this can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html).
You can verify that Elasticsearch is up and running on port 9200 by running:
```
$ curl -X GET http://localhost:9200/
```
You get a response with information about the connection, or a message about failure to connect, in which case you need to look into starting Elasticsearch again.

2. If (and only if) this is the first time you run, you will have to index the dataset of articles. To index you will run the GUI with the first argument set to `True`. For example:
```
$ python gui.py True False
```
The program will start by indexing (takes about X minutes), and then launch the GUI.
If you've already indexed before you should run the gui with first argument set to `False`.

3. The second argument is whether you want personalized search results or not. With this argument set to `False` you will always get search results based on the articles relevance score from Elasticsearch. If it is set to `True` it will also take into account the user's search and click history. When the GUI opens you should enter one of the user's user names (case sensetive). "Johan" is a new and empty profile, but you can also add new ones or use existing ones with saved preferences in the `Users.json` file. After that, you are free to search the dataset for any articles and click on search results that you think are relevant (a short description will be displayed). In personalized mode of the GUI, you can modify the weights for scoring in the bottom.

### Questions?
Contact any of the authors:

Melvin Lundqvist - melvinlu@kth.se,
Linn Ivstam - livstam@kth.se,
Daniel Peng - dpen@kth.se or
Gabriella Dalman - gabdal@kth.se.
