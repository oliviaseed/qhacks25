# from bson import ObjectId
from bson.objectid import ObjectId
from datetime import datetime
from .utils.image import encode_img

USER_REQUIRED_FIELDS = ["first_name", "last_name", "email", "password", "school", "birthday", "gender"]
HOUSE_REQUIRED_FIELDS = ["house_type", "rooms_available", "rent", "utilities_included", "bathrooms", "address", "city", "province", "lease_length", "available_from"]

class User:
    def __init__(self, db):
        self.collection = db.users

    def create(self, user_data):
        """
        Create a new user document in the database.
        """

        profile_picture_encoded = None
        if "profile_picture" in user_data and user_data["profile_picture"]:
            profile_picture_encoded = encode_img(user_data["profile_picture"])
        images_encoded = []
        if "images" in user_data and user_data["images"]:
            for image_path in user_data["images"]:
                images_encoded.append(encode_img(image_path))

        user = {
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "email": user_data["email"],
            "password": user_data["password"],  # TODO: Hash password
            "school": user_data["school"],
            "birthday": user_data["birthday"],
            "gender": user_data["gender"],
            "is_listing": user_data.get("is_listing", False),
            "house_id": None,
            "swipes": [],
            "profile_picture": profile_picture_encoded,
            "images": images_encoded,
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
        
        default_data = {
            "house_type": "",
            "rooms_available": 1,
            "rent": "",
            "utilities_included": "",
            "utilities_cost": "",
            "bathrooms": "",
            "address": "",
            "city": "",
            "province": "",
            "parking": "",
            "pets": "",
            "smoking": "",
            "furnished": "",
            "laundry": "",
            "air_conditioning": "",
            "dishwasher": "",
            "description": "",
            "lease_length": "",
            "available_from": "",
            "images": [],
            "created_at": datetime.utcnow()
        }

        images_encoded = []
        if "images" in house_data and house_data["images"]:
            for image_path in house_data["images"]:
                images_encoded.append(encode_img(image_path))
        house_data["images"] = images_encoded

        house = default_data.update(house_data)
        return self.collection.insert_one(house).inserted_id

    def find_by_id(self, house_id):
        """
        Find a user by their ID.
        """
        if not ObjectId.is_valid(house_id):
            return None
        return self.collection.find_one({"_id": ObjectId(house_id)})
