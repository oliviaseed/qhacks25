from flask import Blueprint, request, jsonify, current_app
from app.models import User, House, USER_REQUIRED_FIELDS
from bson import ObjectId
from ..services.misc_services import encode_img, decode_img

bp = Blueprint("user_routes", __name__)

@bp.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    db = current_app.db
    user_model = User(db)
    user = user_model.find_by_id(user_id)
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # Validate required fields
    for field in USER_REQUIRED_FIELDS:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        db = current_app.db
        user_model = User(db)
        house_model = House(db)

        # If the user is listing a house, add the house first
        house_id = None
        if data.get("is_listing"):
            house_data = data.get("house_listing")
            if not house_data:
                return jsonify({"error": "House listing details are required"}), 400

            required_house_fields = ["type", "rooms_available", "rent", "utilities_included"]
            for field in required_house_fields:
                if field not in house_data or house_data[field] is None:
                    return jsonify({"error": f"Missing required house field: {field}"}), 400

            # Create the house
            house_id = house_model.create(house_data)

        # Create the user
        user_id = user_model.create({
            **data,
            "house_id": house_id
        })

        return jsonify({"message": "User added", "user_id": str(user_id), "house_id": str(house_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/update_user/<user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    try:
        db = current_app.db
        user = db['users'].find_one({"_id": ObjectId(user_id)})
        if user:
            if 'profile_picture' in data and data['profile_picture'] is not None:
                data['profile_picture'] = encode_img(data['profile_picture'])
            images_encoded = []
            if "images" in data and data["images"]:
                for image_path in data["images"]:
                    images_encoded.append(encode_img(image_path))
                data['images'] = images_encoded
            db['users'].update_one({"_id": ObjectId(user_id)}, {"$set": data})
            return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/view_profile_picture/<user_id>', methods=['GET'])
def view_profile_picture(user_id):
    db = current_app.db
    user = db['users'].find_one({"_id": ObjectId(user_id)})
    if user and user.get("profile_picture"):
        return decode_img(user["profile_picture"])
    else:
        return jsonify({"error": "Profile picture not found"}), 404

@bp.route('/view_user_image/<user_id>/<image_index>', methods=['GET'])
def view_user_image(user_id, image_index):
    try:
        db = current_app.db
        user = db['users'].find_one({"_id": ObjectId(user_id)})
        if user and user.get("images"):
            image_index = int(image_index)
            if 0 <= image_index < len(user["images"]):
                return decode_img(user["images"][image_index])
            else:
                return jsonify({"error": "Image index out of range"}), 404
        else:
            return jsonify({"error": "User or images not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# due to multiple inputs, pass inputs in args like
# curl -X GET "http://127.0.0.1:5000/get_users?user_id=679486f52cbb9e9a76e75104&age=25&gender=Male"
@bp.route('/get_users', methods=['GET'])
def get_users():
    user_id = request.args.get('user_id')
    filters = request.args.to_dict()
    filters.pop('user_id', None)  # Remove user_id from filters

    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid logged in user ID"}), 400

    try:
        db = current_app.db
        user_model = User(db)
        
        query = {"_id": {"$ne": ObjectId(user_id)}}
        
        # Apply filters
        for key, value in filters.items():
            query[key] = value

        users = list(db['users'].find(query))
        for user in users:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
            if "house_id" in user and user["house_id"]:
                user["house_id"] = str(user["house_id"])  # Convert house_id to string if it exists

        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500