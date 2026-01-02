
from flask import Blueprint, jsonify, request

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