# OLD LOGIC --- DEPRECATED

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

mongo_user = os.getenv('MONGODB_USER')
mongo_pass = os.getenv('MONGODB_PASS')

print("mongo_user: ", mongo_user)
print("mongo_pass: ", mongo_pass)

# MongoDB configuration
app.config["MONGO_URI"] = f"mongodb+srv://{mongo_user}:{mongo_pass}>@cluster0.wq9eh.mongodb.net/"

mongo = PyMongo(app)
db = mongo.db
print(f"Database connected: {db}")

# Routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get('name') or not data.get('preferences'):
        return jsonify({'error': 'Name and preferences are required'}), 400

    user_id = db.users.insert_one({
        'name': data['name'],
        'preferences': data['preferences'],
        'bio': data.get('bio', ''),
        'matches': []
    }).inserted_id

    return jsonify({'message': 'User created', 'id': str(user_id)}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    return dumps(users), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return dumps(user), 200

@app.route('/match', methods=['POST'])
def find_matches():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_preferences = user['preferences']
    potential_matches = db.users.find({
        '_id': {'$ne': ObjectId(user_id)},
        'preferences': {'$in': user_preferences}
    })

    matches = []
    for match in potential_matches:
        matches.append(match)

    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'matches': [str(match['_id']) for match in matches]}}
    )

    return dumps(matches), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
