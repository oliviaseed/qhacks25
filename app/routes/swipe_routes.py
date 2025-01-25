from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime

bp = Blueprint("swipe_routes", __name__)

@bp.route('/swipe', methods=['POST'])
def swipe():
    data = request.json
    user_id = data.get("user_id")
    target_user_id = data.get("target_user_id")
    action = data.get("action")  # "like" or "dislike"

    # Validate inputs
    if not user_id or not target_user_id or action not in ["like", "dislike"]:
        return jsonify({"error": "Invalid input"}), 400

    if not ObjectId.is_valid(user_id) or not ObjectId.is_valid(target_user_id):
        return jsonify({"error": "Invalid user IDs"}), 400

    try:
        # Fetch the users
        db = current_app.db
        user = db.users.find_one({"_id": ObjectId(user_id)})
        target_user = db.users.find_one({"_id": ObjectId(target_user_id)})

        if not user or not target_user:
            return jsonify({"error": "User(s) not found"}), 404

        # Add the swipe to the user's swipes list
        swipe_entry = {"target_user_id": target_user_id, "status": "disliked" if action == "dislike" else "liked"}
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"swipes": swipe_entry}}
        )

        # If "like", check for a match
        if action == "like":
            # Check if the target user has already liked the current user
            target_swipe = db.users.find_one(
                {"_id": ObjectId(target_user_id), "swipes.target_user_id": user_id, "swipes.status": "liked"}
            )
            if target_swipe:
                # Mark as "matched" for both users
                db.users.update_one(
                    {"_id": ObjectId(user_id), "swipes.target_user_id": target_user_id},
                    {"$set": {"swipes.$.status": "matched"}}
                )
                db.users.update_one(
                    {"_id": ObjectId(target_user_id), "swipes.target_user_id": user_id},
                    {"$set": {"swipes.$.status": "matched"}}
                )

                # Optionally store the match in a separate collection
                match = {
                    "user1_id": user_id,
                    "user2_id": target_user_id,
                    "matched_on": datetime.utcnow()
                }
                match_id = db.matches.insert_one(match).inserted_id

                return jsonify({"message": "It's a match!", "match_id": str(match_id)}), 200

        return jsonify({"message": f"Swipe {action} recorded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# technically, this should be in a separate file, but for simplicity, we'll keep it here
@bp.route('/matches/<user_id>', methods=['GET'])
def get_matches(user_id):
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    try:
        # Fetch the user's matches
        db = current_app.db
        user = db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        matches = db.matches.find({"$or": [
            {"user1_id": user_id},
            {"user2_id": user_id}
        ]})

        match_list = [{"match_id": str(match["_id"]), "user1_id": match["user1_id"], "user2_id": match["user2_id"], "matched_on": match["matched_on"]} for match in matches]

        return jsonify({"matches": match_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
