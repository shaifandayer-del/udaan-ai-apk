Orchestrator.py

import datetime
import json

from AgentConnector import execute_agent


AGENTS = {
    "research": "Research",
    "content": "Content",
    "video": "Video",
    "youtube": "YouTube",
    "social": "Social",
    "analytics": "Analytics",
    "marketing": "Marketing",
    "developer": "Developer",
    "automation": "Automation",
    "creative": "Creative",
}


def _find_agent(agent_name):
    name = str(agent_name or "").strip().lower()

    if name in AGENTS:
        return AGENTS[name]

    for key, value in AGENTS.items():
        if key in name or value.lower() in name:
            return value

    return None


def orchestrate(agent_name, command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Orchestrator",
            "message": "Command is empty."
        }

    selected_agent = _find_agent(agent_name)

    if not selected_agent:
        return {
            "status": "FAILED",
            "agent": "Orchestrator",
            "message": "Unknown agent: " + str(agent_name)
        }

    try:
        result = execute_agent(
            selected_agent,
            command
        )

        if isinstance(result, dict):
            return {
                "status": result.get("status", "FAILED"),
                "agent": selected_agent,
                "command": command,
                "result": result,
                "created_at": datetime.datetime.now().isoformat()
            }

        return {
            "status": "FAILED",
            "agent": selected_agent,
            "command": command,
            "message": "Agent returned an invalid result."
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "agent": selected_agent,
            "command": command,
            "message": str(error),
            "created_at": datetime.datetime.now().isoformat()
        }


def route(agent_name, command):
    return orchestrate(agent_name, command)


def run(agent_name, command):
    return orchestrate(agent_name, command)


def execute(agent_name, command):
    return orchestrate(agent_name, command)


def process(agent_name, command):
    return orchestrate(agent_name, command)


def handle(agent_name, command):
    return orchestrate(agent_name, command)


if __name__ == "__main__":
    agent = input("Agent: ")
    command = input("Command: ")

    print(json.dumps(
        orchestrate(agent, command),
        ensure_ascii=False,
        indent=2
    ))
