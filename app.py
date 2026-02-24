from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

import os
from dotenv import load_dotenv
import urllib.parse

app = Flask(__name__)
CORS(app)

# Route to get all todos from MongoDB
@app.route('/gettodos', methods=['GET'])
def get_todos():
    todos = []
    for todo in todos_collection.find():
        todos.append({
            'id': str(todo.get('_id')),
            'name': todo.get('name'),
            'desc': todo.get('desc')
        })
    return jsonify({'todos': todos})

# Serve the todo.html file from the templates folder at the root URL
@app.route('/')
def serve_todo_html():
    return render_template('todo.html')

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
username = urllib.parse.quote_plus(os.getenv('MONGO_USERNAME'))
password = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD'))
cluster = os.getenv('MONGO_CLUSTER')
dbname = os.getenv('MONGO_DBNAME')
collection_name = os.getenv('MONGO_COLLECTION')

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}.jv8dlwf.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client[dbname]
todos_collection = db[collection_name]

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json()
    item_name = data.get('itemName')
    item_desc = data.get('itemDescription')
    if not item_name or not item_desc:
        return jsonify({'error': 'Missing itemName or itemDescription'}), 400
    todo = {'name': item_name, 'desc': item_desc}
    result = todos_collection.insert_one(todo)

    return jsonify({'message': 'To-Do item submitted successfully', 'todo': {'id': str(result.inserted_id), 'name': todo['name'], 'desc': todo['desc']}}), 201




if __name__ == '__main__':
    app.run(debug=True)
