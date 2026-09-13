AgentHealth.py

import datetime
import importlib


AGENTS = [
    "Research",
    "Content",
    "Video",
    "Creative",
    "YouTube",
    "Social",
    "Analytics",
    "Marketing",
    "Developer",
    "Automation",
]


def check_agent(agent_name):
    name = str(agent_name or "").strip()

    if not name:
        return {
            "name": name,
            "status": "ERROR",
            "message": "Agent name missing."
        }

    try:
        importlib.import_module(name)

        return {
            "name": name,
            "status": "ACTIVE",
            "message": "Agent module loaded successfully.",
            "checked_at": datetime.datetime.now().isoformat()
        }

    except Exception as error:
        return {
            "name": name,
            "status": "ERROR",
            "message": str(error),
            "checked_at": datetime.datetime.now().isoformat()
        }


def check_all_agents():
    results = []

    for agent in AGENTS:
        results.append(
            check_agent(agent)
        )

    return results


def healthy_agents():
    return [
        result
        for result in check_all_agents()
        if result["status"] == "ACTIVE"
    ]


def unhealthy_agents():
    return [
        result
        for result in check_all_agents()
        if result["status"] != "ACTIVE"
    ]


def get_health_summary():
    results = check_all_agents()

    active = sum(
        1
        for result in results
        if result["status"] == "ACTIVE"
    )

    total = len(results)

    return {
        "total_agents": total,
        "active_agents": active,
        "unhealthy_agents": total - active,
        "status": (
            "HEALTHY"
            if active == total
            else "DEGRADED"
        ),
        "checked_at":
            datetime.datetime.now().isoformat(),
        "agents": results
    }


if __name__ == "__main__":
    print(get_health_summary())
