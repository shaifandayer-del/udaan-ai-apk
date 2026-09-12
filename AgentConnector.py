import importlib
import traceback

AGENTS = {
    "Research": "Research",
    "Content": "Content",
    "Video": "Video",
    "YouTube": "YouTube",
    "Social": "Social",
    "Analytics": "Analytics",
    "Marketing": "Marketing",
    "Developer": "Developer",
    "Automation": "Automation",
    "Creative": "Creative",
}

SUPPORTED_FUNCTIONS = [
    "run",
    "execute",
    "process",
    "handle",
    "main",
    "run_agent",
    "research",
    "generate_video",
]

def load_agent(agent_name):
    module_name = AGENTS.get(agent_name)
    if not module_name:
        return None, f"Unknown agent: {agent_name}"
    try:
        return importlib.import_module(module_name), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"

def find_agent_function(module):
    if module is None:
        return None
    for function_name in SUPPORTED_FUNCTIONS:
        function = getattr(module, function_name, None)
        if callable(function):
            return function
    return None

def run_agent(agent_name, command=""):
    module, error = load_agent(agent_name)

    if module is None:
        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": "Agent module load nahi hua.",
            "error": error,
        }

    function = find_agent_function(module)

    if function is None:
        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": "Agent function nahi mila.",
            "error": None,
        }

    try:
        try:
            result = function(command)
        except TypeError:
            result = function()

        if isinstance(result, dict):
            result.setdefault("status", "SUCCESS")
            result.setdefault("agent", agent_name)
            result.setdefault("command", command)
            return result

        return {
            "status": "SUCCESS",
            "agent": agent_name,
            "command": command,
            "message": str(result),
            "result": result,
            "error": None,
        }

    except Exception as exc:
        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": "Agent execution failed.",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }

def execute_agent(agent_name, command=""):
    return run_agent(agent_name, command)

def run(agent_name, command=""):
    return run_agent(agent_name, command)
