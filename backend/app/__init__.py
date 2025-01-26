from flask import Flask
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize MongoDB connection
    try:
        client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)  # 5-second timeout
        # Test the connection
        client.server_info()  # This will raise an error if the connection fails
        app.db = client[app.config["DB_NAME"]]
        print(f"Connected to MongoDB Cluster: {app.config['DB_NAME']}")
    except ServerSelectionTimeoutError as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e
    
    # Register Blueprints
    from app.routes import user_routes, house_routes, swipe_routes, chat_routes, misc_routes
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(house_routes.bp)
    app.register_blueprint(swipe_routes.bp)
    app.register_blueprint(chat_routes.bp)
    app.register_blueprint(misc_routes.bp)

    return app

