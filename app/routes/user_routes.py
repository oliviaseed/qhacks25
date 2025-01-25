from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("user_routes", __name__)

@bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # Example: Save user to MongoDB
    user = {
        "username": data.get("username"),
        "email": data.get("email"),
        "password": data.get("password"),  # NOTE: Hash the password in production
        "school": data.get("school"),
        "age": data.get("age"),
        "gender": data.get("gender"),
        "is_listing": data.get("is_listing"),
        "house_listing": data.get("house_listing") if data.get("is_listing") else None
    }

    try:
        # Access the database using current_app
        user_id = current_app.db.users.insert_one(user).inserted_id
        return jsonify({"message": "User added", "user_id": str(user_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
