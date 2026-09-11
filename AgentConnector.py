import importlib
import traceback

from UdaanDatabase import (
    setup_database,
    add_execution_log
)

from AgentResult import (
    success_result,
    failed_result
)

AGENTS = {
    "Research AI": "Research",
    "Content AI": "Content",
    "Video AI": "Video",
    "YouTube AI": "YouTube",
    "Social AI": "Social",
    "Analytics AI": "Analytics",
    "Marketing AI": "Marketing",
    "Developer AI": "Developer",
    "Automation AI": "Automation",
    "Creative AI": "Creative",
}

SUPPORTED_FUNCTIONS = [
    "run",
    "execute",
    "process",
    "handle",
    "main",
    "run_agent",
]

def load_agent(agent_name):
    if agent_name not in AGENTS:
        print("Unknown agent:", agent_name)
        return None

    module_name = AGENTS[agent_name]

    try:
        module = importlib.import_module(module_name)
        print("Module loaded:", module_name)
        return module

    except Exception as error:
        print("AGENT IMPORT ERROR")
        print("Agent:", agent_name)
        print("Module:", module_name)
        print("Error:", repr(error))
        traceback.print_exc()
        return None

def find_agent_function(module):
    for function_name in SUPPORTED_FUNCTIONS:
        function = getattr(module, function_name, None)

        if callable(function):
            return function_name, function

    return None, None

def save_log(agent, command, status):
    try:
        setup_database()
        add_execution_log(
            agent,
            command,
            status
        )
    except Exception as error:
        print("Execution log error:", repr(error))

def run_agent(agent_name, command):
    module = load_agent(agent_name)

    if module is None:
        result = failed_result(
            agent_name,
            command,
            "Agent module load nahi hua."
        )

        if isinstance(result, dict):
            result["error"] = (
                "Agent import failed. "
                "Render logs mein exact import error dekho."
            )

        save_log(
            agent_name,
            command,
            "FAILED"
        )

        return result

    function_name, function = find_agent_function(module)

    if function is None:
        result = failed_result(
            agent_name,
            command,
            "Supported agent function nahi mila."
        )

        save_log(
            agent_name,
            command,
            "FAILED"
        )

        return result

    try:
        result = function(command)

        if isinstance(result, dict):
            result.setdefault("agent", agent_name)
            result.setdefault("command", command)
            result.setdefault("status", "SUCCESS")
        else:
            result = success_result(
                agent_name,
                command,
                "Agent executed successfully.",
                result
            )

        save_log(
            agent_name,
            command,
            "SUCCESS"
        )

        return result

    except TypeError as first_error:
        print("Agent command signature mismatch:", repr(first_error))

        try:
            result = function()

            if isinstance(result, dict):
                result.setdefault("agent", agent_name)
                result.setdefault("command", command)
                result.setdefault("status", "SUCCESS")
            else:
                result = success_result(
                    agent_name,
                    command,
                    "Agent executed successfully.",
                    result
                )

            save_log(
                agent_name,
                command,
                "SUCCESS"
            )

            return result

        except Exception as error:
            traceback.print_exc()

            save_log(
                agent_name,
                command,
                "FAILED"
            )

            return failed_result(
                agent_name,
                command,
                "Agent execution failed.",
                str(error)
            )

    except Exception as error:
        traceback.print_exc()

        save_log(
            agent_name,
            command,
            "FAILED"
        )

        return failed_result(
            agent_name,
            command,
            "Agent execution failed.",
            str(error)
        )

if __name__ == "__main__":
    agent = input("Agent name: ").strip()
    command = input("Command: ").strip()

    result = run_agent(
        agent,
        command
    )

    print(result)
