import importlib


AGENT_MODULES = {
    "Research": "Research",
    "Content": "Content",
    "Video": "Video",
    "YouTube": "YouTube",
    "Social": "Social",
    "Analytics": "Analytics",
    "Marketing": "Marketing",
    "Developer": "Developer",
    "Automation": "Automation",
    "Creative": "Creative"
}


def _normalize_agent(name):
    name = str(name or "").strip().lower()

    aliases = {
        "research ai": "Research",
        "content ai": "Content",
        "video ai": "Video",
        "youtube ai": "YouTube",
        "social media ai": "Social",
        "social ai": "Social",
        "analytics ai": "Analytics",
        "marketing ai": "Marketing",
        "developer ai": "Developer",
        "automation ai": "Automation",
        "creative ai": "Creative"
    }

    if name in aliases:
        return aliases[name]

    for agent in AGENT_MODULES:
        if name == agent.lower():
            return agent

    return None


def _load_agent(agent_name):
    module_name = AGENT_MODULES.get(agent_name)

    if not module_name:
        return None

    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def execute_agent(agent_name, command):
    selected_agent = _normalize_agent(agent_name)

    if not selected_agent:
        return {
            "status": "FAILED",
            "agent": str(agent_name),
            "message": "Agent not found."
        }

    module = _load_agent(selected_agent)

    if module is None:
        return {
            "status": "FAILED",
            "agent": selected_agent,
            "message": "Agent module could not be loaded."
        }

    for function_name in (
        "run",
        "execute",
        "process",
        "handle"
    ):
        function = getattr(
            module,
            function_name,
            None
        )

        if callable(function):
            try:
                result = function(command)

                if isinstance(result, dict):
                    return result

                return {
                    "status": "SUCCESS",
                    "agent": selected_agent,
                    "command": command,
                    "result": result
                }

            except Exception as error:
                return {
                    "status": "FAILED",
                    "agent": selected_agent,
                    "command": command,
                    "message": str(error)
                }

    return {
        "status": "FAILED",
        "agent": selected_agent,
        "message": "No executable function found."
    }


def connect_agent(agent_name):
    selected_agent = _normalize_agent(agent_name)

    if not selected_agent:
        return {
            "status": "FAILED",
            "message": "Agent not found."
        }

    module = _load_agent(selected_agent)

    if module is None:
        return {
            "status": "FAILED",
            "agent": selected_agent,
            "message": "Agent module could not be loaded."
        }

    return {
        "status": "SUCCESS",
        "agent": selected_agent,
        "module": module.__name__
    }


def run_agent(agent_name, command):
    return execute_agent(agent_name, command)


def execute(agent_name, command):
    return execute_agent(agent_name, command)


def process(agent_name, command):
    return execute_agent(agent_name, command)


def handle(agent_name, command):
    return execute_agent(agent_name, command)
