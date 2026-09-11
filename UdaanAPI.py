import os

from flask import Flask, jsonify, request

from UdaanCommandCenter import execute_command, get_command_center_status


app = Flask(__name__)

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))

FOUNDER_API_KEY = os.environ.get("UDAAN_FOUNDER_API_KEY", "")


def is_authorized():
    provided_key = request.headers.get("X-Udaan-API-Key", "")

    if not FOUNDER_API_KEY:
        return False

    return provided_key == FOUNDER_API_KEY


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "system": "UDAAN AI",
        "status": "ONLINE",
        "message": "UDAAN AI API is running."
    })


@app.route("/status", methods=["GET"])
def status():
    if not is_authorized():
        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    return jsonify(get_command_center_status())


@app.route("/command", methods=["POST"])
def command():
    if not is_authorized():
        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    data = request.get_json(silent=True) or {}
    founder_command = str(data.get("command", "")).strip()

    if not founder_command:
        return jsonify({
            "status": "FAILED",
            "message": "Command empty hai."
        }), 400

    try:
        result = execute_command(founder_command)
        return jsonify(result)
    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "UDAAN command execution failed.",
            "error": str(error)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "system": "UDAAN AI",
        "status": "HEALTHY"
    })


if __name__ == "__main__":
    print("=" * 60)
    print("             UDAAN AI API")
    print("=" * 60)
    print(f"Host : {HOST}")
    print(f"Port : {PORT}")
    print("API  : ONLINE")
    print("=" * 60)

    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )
