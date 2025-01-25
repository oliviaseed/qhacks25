from pymongo import MongoClient

# Replace with your connection string
client = MongoClient("mongodb+srv://ethney:o2iyHC1whuSha1JX@cluster0.wq9eh.mongodb.net/")
db = client.mydatabase

# Example: Insert a document
db.mycollection.insert_one({"name": "Alice", "age": 25})
print("Data inserted into MongoDB Atlas!")
