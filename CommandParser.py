import re
import json

from CommandIntent import detect_intent


def clean_command(command):
    return re.sub(
        r"\s+",
        " ",
        str(command or "").strip()
    )


def parse_command(command):
    command = clean_command(command)

    if not command:
        return {
            "status": "FAILED",
            "message": "Command is empty."
        }

    intent_result = detect_intent(command)

    if not isinstance(intent_result, dict):
        return {
            "status": "FAILED",
            "message": "Intent detection failed."
        }

    intent = intent_result.get(
        "intent",
        "unknown"
    )

    agent_map = {
        "research": "Research",
        "content": "Content",
        "video": "Video",
        "youtube": "YouTube",
        "social": "Social",
        "analytics": "Analytics",
        "marketing": "Marketing",
        "developer": "Developer",
        "automation": "Automation",
        "creative": "Creative"
    }

    agent = agent_map.get(intent)

    if not agent:
        agent = "Main AI"

    return {
        "status": "SUCCESS",
        "command": command,
        "intent": intent,
        "agent": agent,
        "confidence": intent_result.get(
            "confidence",
            0
        ),
        "route": {
            "agent": agent,
            "task": command
        }
    }


def parse(command):
    return parse_command(command)


def classify(command):
    return parse_command(command)


def run(command):
    return parse_command(command)


def execute(command):
    return parse_command(command)


def process(command):
    return parse_command(command)


def handle(command):
    return parse_command(command)


if __name__ == "__main__":
    command = input("UDAAN Command: ")

    print(
        json.dumps(
            parse_command(command),
            ensure_ascii=False,
            indent=2
        )
    )
