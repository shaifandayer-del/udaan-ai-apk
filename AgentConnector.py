# ==========================================
# UDAAN AI - AGENT CONNECTOR
# STEP 72
# ==========================================

import importlib

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

        return None

    module_name = AGENTS[agent_name]

    try:

        return importlib.import_module(
            module_name
        )

    except Exception as error:

        print("❌ Agent load error:")
        print(error)

        return None


def find_agent_function(module):

    for function_name in SUPPORTED_FUNCTIONS:

        function = getattr(
            module,
            function_name,
            None
        )

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

    except Exception:

        pass


def run_agent(agent_name, command):

    print()
    print("================================")
    print("       UDAAN AGENT CONNECTOR")
    print("================================")
    print()

    module = load_agent(agent_name)

    if module is None:

        result = failed_result(
            agent_name,
            command,
            "Agent module load nahi hua."
        )

        save_log(
            agent_name,
            command,
            "FAILED"
        )

        return result

    function_name, function = (
        find_agent_function(module)
    )

    if function is None:

        result = failed_result(
            agent_name,
            command,
            "Supported agent function nahi mila."
        )

        print("⚠️ NO FUNCTION FOUND")
        print("Agent:", agent_name)

        save_log(
            agent_name,
            command,
            "FAILED"
        )

        return result

    print(
        "🤖 Agent:",
        agent_name
    )

    print(
        "⚡ Function:",
        function_name + "()"
    )

    print()

    try:

        result = function(command)

        if isinstance(result, dict):

            result.setdefault(
                "agent",
                agent_name
            )

            result.setdefault(
                "command",
                command
            )

            result.setdefault(
                "status",
                "SUCCESS"
            )

        else:

            result = success_result(
                agent_name,
                command,
                "Agent executed successfully.",
                result
            )

        print("✅ Agent execution completed")

        save_log(
            agent_name,
            command,
            "SUCCESS"
        )

        return result

    except TypeError:

        try:

            result = function()

            if isinstance(result, dict):

                result.setdefault(
                    "agent",
                    agent_name
                )

                result.setdefault(
                    "command",
                    command
                )

                result.setdefault(
                    "status",
                    "SUCCESS"
                )

            else:

                result = success_result(
                    agent_name,
                    command,
                    "Agent executed successfully.",
                    result
                )

            print(
                "✅ Agent execution completed"
            )

            save_log(
                agent_name,
                command,
                "SUCCESS"
            )

            return result

        except Exception as error:

            print(
                "❌ Agent execution error:"
            )

            print(error)

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

        print(
            "❌ Agent execution error:"
        )

        print(error)

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

    print()
    print("================================")
    print("      UDAAN CONNECTOR TEST")
    print("================================")
    print()

    agent = input(
        "Agent name: "
    ).strip()

    command = input(
        "Command: "
    ).strip()

    result = run_agent(
        agent,
        command
    )

    print()
    print("RESULT:")
    print(result)