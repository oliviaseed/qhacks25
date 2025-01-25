from bson import ObjectId
from datetime import datetime
from .services.misc_services import encode_img

USER_REQUIRED_FIELDS = ["first_name", "last_name", "email", "password", "school", "age", "gender"]
HOUSE_REQUIRED_FIELDS = ["type", "rooms_available", "rent", "utilities_included", "bathrooms", "address", "city", "province", "lease_length", "available_from"]

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
            "age": user_data["age"],
            "gender": user_data["gender"],
            "bio": user_data["bio"],
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
        
        images_encoded = []
        if "images" in house_data and house_data["images"]:
            for image_path in house_data["images"]:
                images_encoded.append(encode_img(image_path))

        house = {
            "type": house_data["type"],
            "rooms_available": house_data["rooms_available"],
            "rent": house_data["rent"],
            "utilities_included": house_data["utilities_included"],
            "utilities_cost": house_data["utilities_cost"],
            "bathrooms": house_data["bathrooms"],
            "address": house_data["address"],
            "city": house_data["city"],
            "province": house_data["province"],
            "parking": house_data["parking"],
            "pets": house_data["pets"],
            "smoking": house_data["smoking"],
            "furnished": house_data["furnished"],
            "laundry": house_data["laundry"],
            "air_conditioning": house_data["air_conditioning"],
            "dishwasher": house_data["dishwasher"],
            "description": house_data["description"],
            "lease_length": house_data["lease_length"],
            "available_from": house_data["available_from"],
            "images": images_encoded,
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(house).inserted_id
