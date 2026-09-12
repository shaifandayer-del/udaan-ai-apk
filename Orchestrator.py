import re

from GeminiBrain import ask_gemini
from AgentConnector import run_agent


AGENT_KEYWORDS = {
    "Research": [
        "research",
        "search",
        "latest",
        "trend",
        "information",
        "news",
    ],
    "Content": [
        "content",
        "script",
        "blog",
        "caption",
        "post",
    ],
    "Video": [
        "video",
        "reel",
        "short",
        "render",
    ],
    "YouTube": [
        "youtube",
        "channel",
        "upload",
    ],
    "Social": [
        "instagram",
        "social",
        "facebook",
        "social media",
    ],
    "Analytics": [
        "analytics",
        "performance",
        "report",
        "statistics",
    ],
    "Marketing": [
        "marketing",
        "campaign",
        "growth",
        "promotion",
    ],
    "Developer": [
        "code",
        "developer",
        "software",
        "app",
        "application",
        "program",
    ],
    "Automation": [
        "automation",
        "automate",
        "workflow",
        "schedule",
    ],
    "Creative": [
        "creative",
        "design",
        "idea",
        "thumbnail",
    ],
}


def detect_agent(command):
    text = command.lower()

    scores = {}

    for agent, keywords in AGENT_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            ):
                score += 1

        if score:
            scores[agent] = score

    if not scores:
        return None

    return max(
        scores,
        key=scores.get
    )


def execute_command(command):
    if not command or not command.strip():
        return {
            "status": "FAILED",
            "message": "Command empty hai."
        }

    command = command.strip()

    agent = detect_agent(command)

    if agent:
        result = run_agent(
            agent,
            command
        )

        if result.get("status") == "SUCCESS":
            result["routed_by"] = "UDAAN ORCHESTRATOR"
            return result

    ai_result = ask_gemini(command)

    ai_result["agent"] = "Main AI / Orchestrator"
    ai_result["routed_by"] = "UDAAN ORCHESTRATOR"

    return ai_result


def run(command=""):
    return execute_command(command)


def execute(command=""):
    return execute_command(command)


def process(command=""):
    return execute_command(command)


def handle(command=""):
    return execute_command(command)


def run_agent(command=""):
    return execute_command(command)
```0
