from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "roommate_app")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DEBUG = os.getenv("DEBUG", True)
