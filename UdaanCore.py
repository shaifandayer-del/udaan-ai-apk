# ==========================================
# UDAAN AI - CORE
# Central AI Execution Layer
# STEP 95
# ==========================================

import importlib
import datetime


AGENT_MODULES = {
    "Research AI": "Research",
    "Content AI": "Content",
    "Creative AI": "Creative",
    "Video AI": "Video",
    "Social AI": "Social",
    "YouTube AI": "YouTube",
    "Analytics AI": "Analytics",
    "Marketing AI": "Marketing",
    "Developer AI": "Developer",
    "Automation AI": "Automation",
}


KEYWORDS = {
    "Research AI": [
        "research", "search", "find", "trend",
        "competitor", "information"
    ],

    "Content AI": [
        "content", "script", "article",
        "post idea", "caption", "write"
    ],

    "Creative AI": [
        "creative", "thumbnail", "design",
        "visual", "image"
    ],

    "Video AI": [
        "video", "reel", "short", "editing"
    ],

    "Social AI": [
        "instagram", "facebook",
        "social media", "social"
    ],

    "YouTube AI": [
        "youtube", "youtube video",
        "youtube channel", "upload"
    ],

    "Analytics AI": [
        "analytics", "views",
        "retention", "performance",
        "report", "data"
    ],

    "Marketing AI": [
        "marketing", "campaign",
        "growth", "promotion"
    ],

    "Developer AI": [
        "developer", "coding",
        "code", "app banao",
        "app bana", "android app",
        "software", "software banao",
        "website banao", "build app",
        "create app", "bug", "debug"
    ],

    "Automation AI": [
        "automation", "automate",
        "automatic", "repeat"
    ],
}


def get_core_state():

    return {
        "system": "UDAAN AI CORE",
        "status": "ONLINE",
        "mode": "EXECUTION",
        "timestamp": datetime.datetime.now().isoformat(),
        "agents": list(AGENT_MODULES.keys())
    }


def detect_agent(command):

    command_lower = str(command).lower().strip()

    for agent, words in KEYWORDS.items():

        for word in words:

            if word in command_lower:
                return agent

    return "Main AI"


def find_entry_point(module):

    for function_name in [
        "execute",
        "run",
        "process",
        "handle",
        "research",
        "generate_content",
        "generate_creative",
        "create_video",
        "publish",
        "upload",
    ]:

        function = getattr(
            module,
            function_name,
            None
        )

        if callable(function):
            return function

    return None


def execute_agent(agent_name, command):

    module_name = AGENT_MODULES.get(agent_name)

    if not module_name:

        return {
            "status": "SUCCESS",
            "agent": agent_name,
            "command": command,
            "message": "Main AI received the command."
        }

    try:

        module = importlib.import_module(
            module_name
        )

    except Exception as error:

        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": "Agent module load failed.",
            "error": str(error)
        }

    function = find_entry_point(module)

    if not function:

        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": "Agent function not found."
        }

    try:

        result = function(command)

        # Agent ka original status preserve hoga.
        agent_status = "SUCCESS"

        if isinstance(result, dict):

            agent_status = result.get(
                "status",
                "SUCCESS"
            )

        return {
            "status": agent_status,
            "agent": agent_name,
            "command": command,
            "message": (
                f"{agent_name} processed the command."
            ),
            "result": result
        }

    except Exception as error:

        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": (
                f"{agent_name} execution failed."
            ),
            "error": str(error)
        }


def process_command(command):

    command = str(command).strip()

    if not command:

        return {
            "status": "FAILED",
            "message": "Command empty hai.",
            "core_state": get_core_state()
        }

    agent = detect_agent(command)

    print()
    print("[UDAAN CORE]")
    print("Command :", command)
    print("Agent   :", agent)

    result = execute_agent(
        agent,
        command
    )

    result["core_state"] = get_core_state()

    return result


if __name__ == "__main__":

    print("=" * 60)
    print("          UDAAN AI CORE")
    print("=" * 60)

    print(get_core_state())

    command = input(
        "\nUDAAN command: "
    ).strip()

    print()
    print(process_command(command))
