from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime

bp = Blueprint("chat_routes", __name__)

@bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    match_id = data.get("match_id")
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    message = data.get("message")

    # Validate inputs
    if not match_id or not sender_id or not receiver_id or not message:
        return jsonify({"error": "Missing required fields"}), 400

    if not ObjectId.is_valid(match_id) or not ObjectId.is_valid(sender_id) or not ObjectId.is_valid(receiver_id):
        return jsonify({"error": "Invalid IDs"}), 400

    try:
        db = current_app.db

        # Verify the match exists
        match = db.matches.find_one({"_id": ObjectId(match_id)})
        if not match:
            return jsonify({"error": "Match not found"}), 404

        # Verify the sender and receiver are part of the match
        if sender_id not in [match["user1_id"], match["user2_id"]] or receiver_id not in [match["user1_id"], match["user2_id"]]:
            return jsonify({"error": "Users are not part of this match"}), 403

        # Save the message to the messages collection
        message_doc = {
            "match_id": match_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "timestamp": datetime.utcnow()
        }
        message_id = db.messages.insert_one(message_doc).inserted_id

        # Update the last message in the matches collection
        db.matches.update_one(
            {"_id": ObjectId(match_id)},
            {"$set": {"last_message": {
                "sender_id": sender_id,
                "message": message,
                "timestamp": message_doc["timestamp"]
            }}}
        )

        return jsonify({"message": "Message sent", "message_id": str(message_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/get_messages/<match_id>', methods=['GET'])
def get_messages(match_id):
    if not ObjectId.is_valid(match_id):
        return jsonify({"error": "Invalid match ID"}), 400

    try:
        db = current_app.db

        # Verify the match exists
        match = db.matches.find_one({"_id": ObjectId(match_id)})
        if not match:
            return jsonify({"error": "Match not found"}), 404

        # Fetch messages for the match
        messages = db.messages.find({"match_id": match_id}).sort("timestamp", 1)
        message_list = [{
            "message_id": str(msg["_id"]),
            "sender_id": msg["sender_id"],
            "receiver_id": msg["receiver_id"],
            "message": msg["message"],
            "timestamp": msg["timestamp"]
        } for msg in messages]

        return jsonify({"messages": message_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
