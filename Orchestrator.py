import re
import importlib

from GeminiBrain import ask_gemini
from AgentConnector import run_agent


AGENT_KEYWORDS = {
    "Research": [
        "research", "research karo", "search", "latest",
        "trend", "information", "news", "jankari"
    ],
    "Content": [
        "content", "script", "blog", "caption",
        "post", "title", "description"
    ],
    "Video": [
        "video", "reel", "short", "render",
        "video banao", "video create"
    ],
    "YouTube": [
        "youtube", "channel", "upload",
        "youtube video"
    ],
    "Social": [
        "instagram", "facebook", "social",
        "social media", "post"
    ],
    "Analytics": [
        "analytics", "performance", "report",
        "statistics", "analysis"
    ],
    "Marketing": [
        "marketing", "campaign", "growth",
        "promotion", "promotion karo"
    ],
    "Developer": [
        "code", "developer", "software",
        "app", "application", "program", "build"
    ],
    "Automation": [
        "automation", "automate", "workflow",
        "schedule", "scheduled"
    ],
    "Creative": [
        "creative", "design", "idea",
        "thumbnail", "graphic"
    ],
}


PIPELINE_KEYWORDS = [
    "video banao",
    "video create",
    "youtube video",
    "complete video",
    "full video",
    "content banao",
    "content create",
    "reel banao",
    "short banao",
    "research se video",
    "video workflow",
]


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

    return max(scores, key=scores.get)


def is_pipeline_command(command):
    text = command.lower()

    return any(
        keyword in text
        for keyword in PIPELINE_KEYWORDS
    )


def run_pipeline(command):
    results = []

    pipeline = [
        ("Research", "Research the topic and collect latest useful information."),
        ("Content", "Create the complete content, script, title, description and tags."),
        ("Creative", "Create creative direction, thumbnail concept and visual plan."),
        ("Video", "Create the video from the approved content and visual plan."),
    ]

    for agent_name, instruction in pipeline:
        agent_command = (
            f"{instruction}\n\n"
            f"Founder Request:\n{command}"
        )

        result = run_agent(
            agent_name,
            agent_command
        )

        results.append(result)

        if result.get("status") != "SUCCESS":
            return {
                "status": "FAILED",
                "agent": agent_name,
                "command": command,
                "pipeline": results,
                "message": f"{agent_name} agent failed.",
                "routed_by": "UDAAN ORCHESTRATOR",
            }

    return {
        "status": "SUCCESS",
        "agent": "UDAAN AI Pipeline",
        "command": command,
        "pipeline": results,
        "message": "Research → Content → Creative → Video pipeline completed.",
        "approval_required": True,
        "publish_status": "WAITING_FOR_FOUNDER_APPROVAL",
        "routed_by": "UDAAN ORCHESTRATOR",
    }


def execute_command(command):
    if not command or not command.strip():
        return {
            "status": "FAILED",
            "message": "Command empty hai."
        }

    command = command.strip()

    if is_pipeline_command(command):
        return run_pipeline(command)

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
