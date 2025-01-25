from bson import ObjectId
from datetime import datetime
from .services.misc_services import encode_img

class User:
    def __init__(self, db):
        self.collection = db.users

    def create(self, user_data):
        """
        Create a new user document in the database.
        """
        #TODO: preferences, etc.

        profile_picture_encoded = None
        if "profile_picture" in user_data and user_data["profile_picture"]:
            profile_picture_encoded = encode_img(user_data["profile_picture"])

        user = {
            "username": user_data["username"],
            "email": user_data["email"],
            "password": user_data["password"],  # Hash password in production
            "school": user_data["school"],
            "age": user_data["age"],
            "gender": user_data["gender"],
            "is_listing": user_data.get("is_listing", False),
            "house_id": None,
            "swipes": [],
            "profile_picture": profile_picture_encoded,
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(user).inserted_id

    def find_by_id(self, user_id):
        """
        Find a user by their ID.
        """
        if not ObjectId.is_valid(user_id):
            return None
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def update_is_listing(self, user_id, house_id):
        """
        Update the user's is_listing status and associate a house ID.
        """
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_listing": True, "house_id": house_id}}
        )


class House:
    def __init__(self, db):
        self.collection = db.houses

    def create(self, house_data):
        """
        Create a new house document in the database.
        """
        
        images_encoded = []
        if "images" in house_data and house_data["images"]:
            for image_path in house_data["images"]:
                images_encoded.append(encode_img(image_path))

        house = {
            "type": house_data["type"],
            "rooms_available": house_data["rooms_available"],
            "rent": house_data["rent"],
            "utilities_included": house_data["utilities_included"],
            "images": images_encoded,
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(house).inserted_id
