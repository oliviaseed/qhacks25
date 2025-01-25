from pymongo import MongoClient

# Connection string
client = MongoClient("mongodb+srv://ethney:o2iyHC1whuSha1JX@cluster0.wq9eh.mongodb.net/")

# Access the database and collection
db = client['users']  # Database name
users_collection = db['user']  # Collection name

try:
    # Test the connection
    print("Attempting to connect to the database...")
    client.admin.command('ping')  # Pings the MongoDB server
    print("Connection successful!")

    # Test an insert
    test_document = {"username": "testuser", "password": "testpass"}
    result = users_collection.insert_one(test_document)
    print(f"Test document inserted with ID: {result.inserted_id}")

    # Test a find
    print("Testing a query...")
    for user in users_collection.find():
        print(user)
    
    # # Clean up the test document (optional)
    # users_collection.delete_one({"_id": result.inserted_id})
    # print("Test document cleaned up.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
