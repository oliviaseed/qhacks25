from flask import Blueprint, request, jsonify, current_app, send_file
from app.models import User, House
import base64
from bson import ObjectId
import io

bp = Blueprint("user_routes", __name__)

@bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # Validate required fields
    required_fields = ["username", "email", "password", "school", "age", "gender"]
    for field in required_fields:
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

@bp.route('/view_profile_picture/<user_id>', methods=['GET'])
def view_profile_picture(user_id):
    db = current_app.db
    user = db['users'].find_one({"_id": ObjectId(user_id)})
    print("db: ", db)
    print("User: ", user)
    if user and user.get("profile_picture"):
        profile_picture_encoded = user["profile_picture"]
        profile_picture_decoded = base64.b64decode(profile_picture_encoded)
        return send_file(io.BytesIO(profile_picture_decoded), mimetype='image/jpeg')
    else:
        return jsonify({"error": "Profile picture not found"}), 404
