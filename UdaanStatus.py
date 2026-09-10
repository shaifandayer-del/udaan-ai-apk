import sqlite3
import importlib
import os


DB_NAME = "udaan_ai.db"


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
    "Creative AI": "Creative"
}


CORE_MODULES = [
    "UdaanCore",
    "AgentConnector",
    "AgentResult",
    "TaskManager",
    "FounderApproval",
    "UdaanMemory",
    "UdaanSecurity",
    "GeminiBrain"
]


TABLES = [
    "tasks",
    "approvals",
    "execution_logs",
    "memories"
]


def check_database():
    if not os.path.exists(DB_NAME):
        return "OFFLINE"

    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        for table in TABLES:
            cursor.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name=?",
                (table,)
            )

            if cursor.fetchone() is None:
                connection.close()
                return "WARNING"

        connection.close()
        return "ONLINE"

    except Exception:
        return "ERROR"


def check_modules():
    results = {}

    for module_name in CORE_MODULES:
        try:
            importlib.import_module(module_name)
            results[module_name] = "ONLINE"
        except Exception:
            results[module_name] = "ERROR"

    return results


def check_agents():
    results = {}

    functions = [
        "run",
        "execute",
        "process",
        "handle",
        "main",
        "run_agent"
    ]

    for agent_name, module_name in AGENTS.items():

        try:
            module = importlib.import_module(module_name)

            found = False

            for function_name in functions:
                function = getattr(module, function_name, None)

                if callable(function):
                    found = True
                    break

            if found:
                results[agent_name] = "ONLINE"
            else:
                results[agent_name] = "NO_FUNCTION"

        except Exception:
            results[agent_name] = "ERROR"

    return results


def health_check():
    database_status = check_database()
    modules = check_modules()
    agents = check_agents()

    core_online = sum(
        1 for status in modules.values()
        if status == "ONLINE"
    )

    agent_online = sum(
        1 for status in agents.values()
        if status == "ONLINE"
    )

    total_core = len(CORE_MODULES)
    total_agents = len(AGENTS)

    all_online = (
        database_status == "ONLINE"
        and core_online == total_core
        and agent_online == total_agents
    )

    return {
        "system": "ONLINE" if all_online else "NEEDS_ATTENTION",
        "database": database_status,
        "core_online": core_online,
        "core_total": total_core,
        "agents_online": agent_online,
        "agents_total": total_agents,
        "core": modules,
        "agents": agents
    }


def get_status():
    return health_check()


def system_status():
    return health_check()


def show_status():

    status = health_check()

    print()
    print("=" * 55)
    print("              UDAAN AI")
    print("          SYSTEM STATUS CENTER")
    print("=" * 55)

    print()
    print("DATABASE")
    print("   Status :", status["database"])

    print()
    print("CORE MODULES")

    for module, module_status in status["core"].items():

        icon = "🟢" if module_status == "ONLINE" else "🔴"

        print(
            f"   {icon} {module:<20} {module_status}"
        )

    print(
        f"   CORE: {status['core_online']}/"
        f"{status['core_total']} ONLINE"
    )

    print()
    print("AI AGENTS")

    for agent, agent_status in status["agents"].items():

        if agent_status == "ONLINE":
            icon = "🟢"
        elif agent_status == "NO_FUNCTION":
            icon = "🟡"
        else:
            icon = "🔴"

        print(
            f"   {icon} {agent:<20} {agent_status}"
        )

    print(
        f"   AGENTS: {status['agents_online']}/"
        f"{status['agents_total']} ONLINE"
    )

    print()
    print("=" * 55)

    if status["system"] == "ONLINE":
        print("🚀 UDAAN AI SYSTEM: ONLINE")
        print("🟢 ALL CORE SYSTEMS READY")
    else:
        print("⚠️ UDAAN AI SYSTEM: NEEDS ATTENTION")

    print("=" * 55)
    print()


if __name__ == "__main__":
    show_status()