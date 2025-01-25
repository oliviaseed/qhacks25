from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from app.models import User, House, HOUSE_REQUIRED_FIELDS
from ..services.misc_services import encode_img, decode_img

bp = Blueprint("house_routes", __name__)

@bp.route('/add_house/<user_id>', methods=['POST'])
def add_house(user_id):
    # Validate the user_id
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    # Parse the request data
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request, no data provided"}), 400

    for field in HOUSE_REQUIRED_FIELDS:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
        
    try:
        db = current_app.db
        user_model = User(db)
        house_model = House(db)

        required_fields = ["type", "rooms_available", "rent", "utilities_included"]
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({"error": f"Missing required house field: {field}"}), 400

        # Create the house
        house_id = house_model.create(data)
        user_model.update_is_listing(user_id, house_id)

        return jsonify({"message": "House added", "house_id": str(house_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/update_house/<house_id>', methods=['PATCH'])
def update_house(house_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    try:
        db = current_app.db
        house = db['houses'].find_one({"_id": ObjectId(house_id)})
        if house:
            if "images" in data and data["images"]:
                images_encoded = []
                for image_path in data["images"]:
                    images_encoded.append(encode_img(image_path))
                data['images'] = images_encoded
            db['houses'].update_one({"_id": ObjectId(house_id)}, {"$set": data})
            return jsonify({"message": "House listing updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/view_house_image/<house_id>/<image_index>', methods=['GET'])
def view_house_image(house_id, image_index):
    try:
        db = current_app.db
        house = db['houses'].find_one({"_id": ObjectId(house_id)})
        if house and house.get("images"):
            image_index = int(image_index)
            if 0 <= image_index < len(house["images"]):
                return decode_img(house["images"][image_index])
            else:
                return jsonify({"error": "Image index out of range"}), 404
        else:
            return jsonify({"error": "House or images not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    