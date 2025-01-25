from flask import Blueprint, request, jsonify, current_app
from app.models import User, House

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
