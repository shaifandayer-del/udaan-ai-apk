import os

from flask import Flask, jsonify, request

from UdaanCommandCenter import (
    execute_command,
    get_command_center_status
)

from FounderApproval import (
    get_pending_approvals,
    get_approval
)

from FounderApprovalExecutor import (
    approve_and_execute,
    reject_request
)


app = Flask(__name__)

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))

FOUNDER_API_KEY = os.environ.get(
    "UDAAN_FOUNDER_API_KEY",
    ""
)


# ==========================================
# SECURITY
# ==========================================

def is_authorized():

    provided_key = request.headers.get(
        "X-Udaan-API-Key",
        ""
    )

    return (
        bool(FOUNDER_API_KEY)
        and provided_key == FOUNDER_API_KEY
    )


# ==========================================
# COMMAND
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "system": "UDAAN AI",
        "status": "ONLINE",
        "message": "UDAAN AI API is running."
    })


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "system": "UDAAN AI",
        "status": "HEALTHY"
    })


@app.route("/status", methods=["GET"])
def status():

    if not is_authorized():

        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    return jsonify(
        get_command_center_status()
    )


@app.route("/command", methods=["POST"])
def command():

    if not is_authorized():

        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    founder_command = str(
        data.get("command", "")
    ).strip()

    if not founder_command:

        return jsonify({
            "status": "FAILED",
            "message": "Command empty hai."
        }), 400

    try:

        result = execute_command(
            founder_command
        )

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "status": "FAILED",
            "message": "UDAAN command execution failed.",
            "error": str(error)
        }), 500


# ==========================================
# FOUNDER APPROVALS
# ==========================================

@app.route("/approvals", methods=["GET"])
def approvals():

    if not is_authorized():

        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    return jsonify({
        "status": "SUCCESS",
        "approvals": get_pending_approvals()
    })


@app.route(
    "/approvals/<approval_id>",
    methods=["GET"]
)
def approval_details(approval_id):

    if not is_authorized():

        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    approval = get_approval(
        approval_id
    )

    if not approval:

        return jsonify({
            "status": "FAILED",
            "message": "Approval ID not found.",
            "approval_id": approval_id
        }), 404

    return jsonify({
        "status": "SUCCESS",
        "approval": approval
    })


@app.route(
    "/approvals/<approval_id>/approve",
    methods=["POST"]
)
def approve_approval(approval_id):

    if not is_authorized():

        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    try:

        result = approve_and_execute(
            approval_id
        )

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "status": "FAILED",
            "message": "Approval execution failed.",
            "approval_id": approval_id,
            "error": str(error)
        }), 500


@app.route(
    "/approvals/<approval_id>/reject",
    methods=["POST"]
)
def reject_approval(approval_id):

    if not is_authorized():

        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Founder API Key required."
        }), 401

    try:

        result = reject_request(
            approval_id
        )

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "status": "FAILED",
            "message": "Approval rejection failed.",
            "approval_id": approval_id,
            "error": str(error)
        }), 500


# ==========================================
# LOCAL SERVER
# ==========================================

if __name__ == "__main__":

    print("=" * 60)
    print("                 UDAAN AI API")
    print("=" * 60)
    print()
    print("Host :", HOST)
    print("Port :", PORT)
    print("API  : ONLINE")
    print("Founder Approval API : ENABLED")
    print()
    print("=" * 60)

    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )
