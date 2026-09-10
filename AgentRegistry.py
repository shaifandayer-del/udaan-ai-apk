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


def get_agents():
    return AGENTS


def check_agent(agent_name):
    if agent_name not in AGENTS:
        return {
            "agent": agent_name,
            "status": "NOT_REGISTERED"
        }

    module_name = AGENTS[agent_name]

    try:
        importlib.import_module(module_name)

        return {
            "agent": agent_name,
            "file": module_name + ".py",
            "status": "ONLINE"
        }

    except Exception as error:

        return {
            "agent": agent_name,
            "file": module_name + ".py",
            "status": "ERROR",
            "error": str(error)
        }


def show_agents():

    print()
    print("================================")
    print("       UDAAN AI AGENT REGISTRY")
    print("================================")
    print()

    for agent_name in AGENTS:

        result = check_agent(agent_name)

        if result["status"] == "ONLINE":
            print("🟢", agent_name, "-> ONLINE")

        elif result["status"] == "ERROR":
            print("🔴", agent_name, "-> ERROR")
            print("   Reason:", result["error"])

        else:
            print("⚪", agent_name, "-> NOT REGISTERED")

    print()
    print("================================")
    print()


if __name__ == "__main__":
    show_agents()