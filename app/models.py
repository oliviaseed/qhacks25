from bson.objectid import ObjectId

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "age": user["age"],
        "gender": user["gender"],
        "is_listing": user.get("is_listing", False),
        "house_id": user.get("house_id")
    }

def serialize_house(house):
    return {
        "id": str(house["_id"]),
        "type": house["type"],
        "rooms_available": house["rooms_available"],
        "rent": house["rent"],
        "utilities_included": house["utilities_included"]
    }
