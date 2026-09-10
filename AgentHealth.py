# ==========================================
# UDAAN AI - ADVANCED AGENT HEALTH
# STEP 58
# ==========================================

import importlib


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


def check_agent(agent_name, module_name):

    result = {
        "agent": agent_name,
        "file": module_name + ".py",
        "status": "ERROR",
        "function": None,
        "error": None,
    }

    try:

        module = importlib.import_module(module_name)

        found_function = None

        for function_name in SUPPORTED_FUNCTIONS:

            function = getattr(module, function_name, None)

            if callable(function):
                found_function = function_name
                break

        if found_function:

            result["status"] = "ONLINE"
            result["function"] = found_function

        else:

            result["status"] = "NO_FUNCTION"

        return result

    except ModuleNotFoundError as error:

        result["status"] = "FILE_MISSING"
        result["error"] = str(error)

        return result

    except Exception as error:

        result["status"] = "ERROR"
        result["error"] = str(error)

        return result


def check_all_agents():

    results = []

    for agent_name, module_name in AGENTS.items():

        result = check_agent(
            agent_name,
            module_name
        )

        results.append(result)

    return results


def show_health():

    print()
    print("================================")
    print("     UDAAN AI AGENT HEALTH")
    print("          STEP 58")
    print("================================")
    print()

    results = check_all_agents()

    online = 0
    no_function = 0
    missing = 0
    errors = 0

    for result in results:

        status = result["status"]

        if status == "ONLINE":

            online += 1

            print(
                "🟢",
                result["agent"],
                "-> ONLINE",
                "|",
                result["function"] + "()"
            )

        elif status == "NO_FUNCTION":

            no_function += 1

            print(
                "🟡",
                result["agent"],
                "-> NO_FUNCTION"
            )

        elif status == "FILE_MISSING":

            missing += 1

            print(
                "⚪",
                result["agent"],
                "-> FILE MISSING"
            )

            print(
                "   File:",
                result["file"]
            )

        else:

            errors += 1

            print(
                "🔴",
                result["agent"],
                "-> ERROR"
            )

            if result["error"]:
                print(
                    "   Reason:",
                    result["error"]
                )

    print()
    print("--------------------------------")
    print("📊 TOTAL AGENTS :", len(results))
    print("🟢 ONLINE       :", online)
    print("🟡 NO_FUNCTION  :", no_function)
    print("⚪ FILE MISSING :", missing)
    print("🔴 ERRORS       :", errors)
    print("--------------------------------")
    print()

    if no_function == 0 and missing == 0 and errors == 0:

        print("🎉 ALL AGENTS HEALTHY")

    else:

        print("⚠️ AGENT ISSUES DETECTED")

        if no_function > 0:
            print(
                "➡️ Next repair target:",
                no_function,
                "NO_FUNCTION agent(s)"
            )

        if missing > 0:
            print(
                "➡️ Missing files:",
                missing
            )

        if errors > 0:
            print(
                "➡️ Error agents:",
                errors
            )

    print()


if __name__ == "__main__":

    show_health()