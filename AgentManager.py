from AgentRegistry import get_agents, check_agent


def list_agents():
    return list(get_agents().keys())


def get_agent_status(agent_name):
    return check_agent(agent_name)


def show_agent_manager():

    print()
    print("================================")
    print("       UDAAN AI AGENT MANAGER")
    print("================================")
    print()

    agents = list_agents()

    print("🤖 Total Registered Agents:", len(agents))
    print()

    for agent in agents:

        status = get_agent_status(agent)

        if status["status"] == "ONLINE":
            print("🟢", agent, "-> ONLINE")

        elif status["status"] == "ERROR":
            print("🔴", agent, "-> ERROR")
            print("   Reason:", status.get("error", "Unknown error"))

        else:
            print("⚪", agent, "->", status["status"])

    print()
    print("================================")
    print()


if __name__ == "__main__":
    show_agent_manager()