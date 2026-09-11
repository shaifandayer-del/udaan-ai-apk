import os
import importlib
from flask import Flask, jsonify, request
from UdaanCommandCenter import execute_command, get_command_center_status
from FounderApproval import get_pending_approvals, get_approval
from FounderApprovalExecutor import approve_and_execute, reject_request

app = Flask(__name__)

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "10000"))
FOUNDER_API_KEY = os.getenv("UDAAN_FOUNDER_API_KEY", "")

def check_api_key():
    if not FOUNDER_API_KEY:
        return False
    return request.headers.get("X-Udaan-API-Key", "") == FOUNDER_API_KEY

def unauthorized():
    return jsonify({
        "status": "UNAUTHORIZED",
        "message": "Founder API key required."
    }), 401

def get_dynamic_agents():
    agent_files = [
        ("Research", "Research AI", "Research & trends"),
        ("Content", "Content AI", "Scripts & captions"),
        ("Video", "Video AI", "Video generation"),
        ("YouTube", "YouTube AI", "YouTube workflow"),
        ("Social", "Social Media AI", "Instagram & social media"),
        ("Analytics", "Analytics AI", "Insights & reports"),
        ("Marketing", "Marketing AI", "Campaigns & growth"),
        ("Developer", "Developer AI", "Apps & software"),
        ("Automation", "Automation AI", "Workflows & automation"),
        ("Creative", "Creative AI", "Ideas & design")
    ]

    agents = []

    for module_name, display_name, description in agent_files:
        item = {
            "name": display_name,
            "module": module_name,
            "description": description,
            "status": "OFFLINE",
            "functions": []
        }

        try:
            module = importlib.import_module(module_name)
            functions = []

            for name in dir(module):
                if name.startswith("_"):
                    continue

                try:
                    value = getattr(module, name)
                except Exception:
                    continue

                if callable(value):
                    functions.append(name)

            item["status"] = "ONLINE"
            item["functions"] = sorted(set(functions))

        except Exception as error:
            item["error"] = str(error)

        agents.append(item)

    online_count = sum(
        1 for agent in agents
        if agent["status"] == "ONLINE"
    )

    return {
        "status": "SUCCESS",
        "count": len(agents),
        "online": online_count,
        "offline": len(agents) - online_count,
        "agents": agents
    }

@app.get("/")
def home():
    return jsonify({
        "name": "UDAAN AI API",
        "status": "ONLINE",
        "service": "AI Command Center",
        "version": "1.0",
        "message": "UDAAN AI backend is running."
    })

@app.get("/health")
def health():
    return jsonify({
        "status": "ONLINE",
        "service": "UDAAN AI",
        "api": "READY"
    })

@app.get("/status")
def status():
    if not check_api_key():
        return unauthorized()

    try:
        result = get_command_center_status()

        return jsonify({
            "status": "ONLINE",
            "service": "UDAAN AI",
            "command_center": result
        })

    except Exception as error:
        return jsonify({
            "status": "ERROR",
            "service": "UDAAN AI",
            "error": str(error)
        }), 500

@app.get("/agents")
def agents_endpoint():
    if not check_api_key():
        return unauthorized()

    try:
        return jsonify(get_dynamic_agents())

    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "Agent discovery failed.",
            "error": str(error)
        }), 500

@app.post("/command")
def command_endpoint():
    if not check_api_key():
        return unauthorized()

    try:
        data = request.get_json(silent=True) or {}
        command = str(data.get("command", "")).strip()

        if not command:
            return jsonify({
                "status": "FAILED",
                "message": "Command is empty."
            }), 400

        result = execute_command(command)
        return jsonify(result)

    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "UDAAN command execution failed.",
            "error": str(error)
        }), 500

@app.get("/approvals")
def approvals_endpoint():
    if not check_api_key():
        return unauthorized()

    try:
        approvals = get_pending_approvals()

        return jsonify({
            "status": "SUCCESS",
            "count": len(approvals),
            "approvals": approvals
        })

    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "Unable to load approvals.",
            "error": str(error)
        }), 500

@app.get("/approvals/<approval_id>")
def approval_endpoint(approval_id):
    if not check_api_key():
        return unauthorized()

    try:
        approval = get_approval(approval_id)

        if not approval:
            return jsonify({
                "status": "FAILED",
                "message": "Approval ID not found."
            }), 404

        return jsonify({
            "status": "SUCCESS",
            "approval": approval
        })

    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "Unable to load approval.",
            "error": str(error)
        }), 500

@app.post("/approve")
def approve_endpoint():
    if not check_api_key():
        return unauthorized()

    try:
        data = request.get_json(silent=True) or {}
        approval_id = str(data.get("approval_id", "")).strip()

        if not approval_id:
            return jsonify({
                "status": "FAILED",
                "message": "approval_id is required."
            }), 400

        return jsonify(approve_and_execute(approval_id))

    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "Approval execution failed.",
            "error": str(error)
        }), 500

@app.post("/reject")
def reject_endpoint():
    if not check_api_key():
        return unauthorized()

    try:
        data = request.get_json(silent=True) or {}
        approval_id = str(data.get("approval_id", "")).strip()

        if not approval_id:
            return jsonify({
                "status": "FAILED",
                "message": "approval_id is required."
            }), 400

        return jsonify(reject_request(approval_id))

    except Exception as error:
        return jsonify({
            "status": "FAILED",
            "message": "Approval rejection failed.",
            "error": str(error)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "FAILED",
        "message": "Endpoint not found."
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "status": "FAILED",
        "message": "HTTP method not allowed."
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "FAILED",
        "message": "Internal server error.",
        "error": str(error)
    }), 500

if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT
    )
