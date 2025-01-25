from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

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

    # Ensure required fields for the house listing are provided
    required_fields = ["type", "rooms_available", "rent", "utilities_included"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Build the house document
    house = {
        "type": data.get("type"),
        "rooms_available": data.get("rooms_available"),
        "rent": data.get("rent"),
        "utilities_included": data.get("utilities_included")
    }

    try:
        # Insert the house into the database
        house_id = current_app.db.houses.insert_one(house).inserted_id

        # Update the user's document to reference the new house
        result = current_app.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_listing": True, "house_id": house_id}}
        )

        if result.matched_count == 0:
            # If no user is found with the given user_id, return an error
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "House added to user", "house_id": str(house_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
