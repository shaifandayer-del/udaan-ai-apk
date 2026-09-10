# PythonCoreHealth.py

import importlib
import json
from datetime import datetime


MODULE_GROUPS = {

    "CORE": [
        "UdaanCore",
        "UdaanRouter",
        "AgentConnector",
        "AgentRegistry",
        "AgentManager",
        "SmartAgentMatcher",
        "CommandIntent",
        "TaskManager",
        "FounderApproval",
        "ApprovalDatabase",
        "UdaanDatabase",
        "UdaanMemory",
        "UdaanHistory",
        "ExecutionLogs",
        "AgentResult",
        "GeminiBrain",
        "UdaanSecurity",
        "UdaanStatus",
        "UdaanAPI",
        "UdaanCommandCenter"
    ],

    "AGENTS": [
        "Research",
        "Content",
        "Video",
        "YouTube",
        "Social",
        "Analytics",
        "Marketing",
        "Developer",
        "Automation",
        "Creative"
    ],

    "VIDEO": [
        "VideoPreview",
        "VideoApprovalController",
        "VideoShareController",
        "AndroidShareBridge"
    ]
}


REPORT_FILE = "udaan_python_health.json"


def check_module(name):

    try:

        module = importlib.import_module(name)

        return {
            "name": name,
            "status": "ONLINE",
            "error": None,
            "functions": [
                item
                for item in dir(module)
                if callable(getattr(module, item, None))
                and not item.startswith("_")
            ]
        }

    except Exception as error:

        return {
            "name": name,
            "status": "ERROR",
            "error": str(error),
            "functions": []
        }


def run_health_check():

    print()
    print("=" * 65)
    print("          UDAAN AI — PYTHON CORE HEALTH")
    print("=" * 65)

    report = {
        "timestamp": datetime.now().isoformat(),
        "groups": {},
        "total": 0,
        "online": 0,
        "errors": 0
    }

    for group_name, modules in MODULE_GROUPS.items():

        print()
        print(f"🔹 {group_name}")
        print("-" * 65)

        group_results = []

        for module_name in modules:

            result = check_module(module_name)

            group_results.append(result)

            report["total"] += 1

            if result["status"] == "ONLINE":

                report["online"] += 1

                print(
                    f"✅ {module_name:<35} ONLINE"
                )

            else:

                report["errors"] += 1

                print(
                    f"❌ {module_name:<35} ERROR"
                )

                print(
                    f"   {result['error']}"
                )

        report["groups"][group_name] = group_results

    total = report["total"]
    online = report["online"]

    if total > 0:

        health = round(
            (online / total) * 100,
            2
        )

    else:

        health = 0

    report["health_percent"] = health

    if report["errors"] == 0:

        report["overall_status"] = "HEALTHY"

    elif health >= 80:

        report["overall_status"] = "MOSTLY_HEALTHY"

    else:

        report["overall_status"] = "NEEDS_FIXES"

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("=" * 65)
    print("                 HEALTH SUMMARY")
    print("=" * 65)

    print()
    print("Total Modules :", total)
    print("Online        :", online)
    print("Errors        :", report["errors"])
    print("Health        :", f"{health}%")
    print("Status        :", report["overall_status"])

    print()
    print("📄 Report:")
    print(REPORT_FILE)

    print()
    print("=" * 65)

    return report


if __name__ == "__main__":

    run_health_check()