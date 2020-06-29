from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
import datetime
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)
# Where 'mongo' is the name of the swarm network (docker network ls)
client = MongoClient('mongodb://mongo:27017/')

db = client.test_database
collection = db.test_collection

es = Elasticsearch(
	['elasticsearch'],
		http_auth=('elastic', 'Z6dm5Ff3br86jDnvjaoZbYQv')
	)

posts = db.posts

@app.route('/')
def index():

	# Creating an index
	es.indices.create(index="authors", ignore=400)

	if posts.find_one() != None:
		_items = posts.find()
		items = [item for item in _items]
	else:
		items = []
		
	print("Items", items)

	return render_template('index.html', items=items)


@app.route('/new', methods=['POST'])
def new():
	post = {
	"author": request.form['author'],
	"text": request.form['text'],
	"tags": request.form['tags'],
	"data" : str(datetime.datetime.utcnow())
	}

	# Inserting form data into indexes
	es.index(index='authors', body=post)

	print("POST", post, flush=True)

	post_id = posts.insert_one(post).inserted_id
	# Inserting in the index

	print("ID", post_id, flush=True)

	#serialized = json.dumps(post)
	
	return redirect(url_for('index'))

@app.route('/search', methods=['GET','POST'])
def search():

	# Doing a search in the index for authors
	res = es.search(index='authors', body={'from':0, 'size':2, 
			'query':{'match':{'author':request.form['busca']}}})
	
	#return render_template('search.html', res=res)
	return jsonify(res['hits']['hits'])

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5000', debug=True)