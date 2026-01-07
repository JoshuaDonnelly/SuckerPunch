import os
import mysql.connector
from flask import Blueprint, request, session, jsonify
from .db import get_db

api = Blueprint("api", __name__)


@api.route("/api/pubnub/web-token")
def web_token():
    # Return a placeholder since tokens aren't needed
    return jsonify({"token": "no-token-required"})


@api.route("/api/pubnub/pi-token")
def pi_token():
    # Return a placeholder since tokens aren't needed
    # keep the device check for other purposes
    if request.headers.get("X-DEVICE") != "PI":
        return jsonify({"error": "unauthorized"}), 403
    
    return jsonify({"token": "no-token-required"})


@api.route("/api/pubnub/status")
def pubnub_status():
    """Check PubNub connection status"""
    return jsonify({
        "status": "active",
        "access_manager": "disabled",
        "note": "No tokens required for publish/subscribe"
    })

@api.route("/api/sessions/save", methods=["POST"])
def save_session():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    try:
        title = data["title"]
        description = data.get("description", "")
        focus = data.get("focus", "")
        minutes = int(data["minutes"])
    except (KeyError, ValueError) as e:
        return jsonify({"error": f"Invalid data: {str(e)}"}), 400

    user_id = session["user_id"]


    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO shadow_sessions
        (user_id, title, description, focus, minutes, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """,
        (user_id, title, description, focus, minutes)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "saved"}), 201

