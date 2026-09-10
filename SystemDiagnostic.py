# ==========================================
# UDAAN AI - SYSTEM DIAGNOSTIC
# STEP 74
# ==========================================

import importlib


MODULES = [
    "UdaanDatabase",
    "UdaanMemory",
    "TaskManager",
    "FounderApproval",
    "AgentResult",
    "AgentConnector",
    "UdaanCore",
    "GeminiBrain",
    "CommandIntent",
    "SmartAgentMatcher",
]


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


def check_module(name):

    try:

        importlib.import_module(name)

        return True, ""

    except Exception as error:

        return False, str(error)


def check_agent(name, module_name):

    try:

        module = importlib.import_module(
            module_name
        )

        function = getattr(
            module,
            "run",
            None
        )

        if callable(function):

            return True, "run()"

        return False, "run() missing"

    except Exception as error:

        return False, str(error)


def run_diagnostic():

    print()
    print("================================")
    print("       UDAAN AI DIAGNOSTIC")
    print("           STEP 74")
    print("================================")
    print()

    module_pass = 0
    module_fail = 0

    agent_pass = 0
    agent_fail = 0

    # --------------------------------------
    # CORE MODULES
    # --------------------------------------

    print("🧠 CORE MODULE CHECK")
    print()

    for module_name in MODULES:

        ok, message = check_module(
            module_name
        )

        if ok:

            module_pass += 1

            print(
                "🟢",
                module_name,
                "-> ONLINE"
            )

        else:

            module_fail += 1

            print(
                "🔴",
                module_name,
                "-> ERROR"
            )

            print(
                "   Reason:",
                message
            )

    # --------------------------------------
    # AGENTS
    # --------------------------------------

    print()
    print("--------------------------------")
    print("🤖 AGENT CHECK")
    print("--------------------------------")
    print()

    for agent_name, module_name in AGENTS.items():

        ok, message = check_agent(
            agent_name,
            module_name
        )

        if ok:

            agent_pass += 1

            print(
                "🟢",
                agent_name,
                "-> ONLINE |",
                message
            )

        else:

            agent_fail += 1

            print(
                "🔴",
                agent_name,
                "-> ERROR"
            )

            print(
                "   Reason:",
                message
            )

    # --------------------------------------
    # SUMMARY
    # --------------------------------------

    print()
    print("================================")
    print("       DIAGNOSTIC SUMMARY")
    print("================================")
    print()

    print(
        "🧠 Core Modules:",
        module_pass,
        "/",
        len(MODULES)
    )

    print(
        "🤖 Agents:",
        agent_pass,
        "/",
        len(AGENTS)
    )

    print(
        "🔴 Module Errors:",
        module_fail
    )

    print(
        "🔴 Agent Errors:",
        agent_fail
    )

    print()

    if (
        module_fail == 0
        and agent_fail == 0
    ):

        print(
            "🎉 UDAAN AI SYSTEM HEALTHY"
        )

    else:

        print(
            "⚠️ UDAAN AI NEEDS ATTENTION"
        )

    print()


if __name__ == "__main__":

    run_diagnostic()