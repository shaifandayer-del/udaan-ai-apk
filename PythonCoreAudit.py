# PythonCoreAudit.py

import importlib
import os
from datetime import datetime


CORE_MODULES = [
    "UdaanCore",
    "UdaanRouter",
    "UdaanMain",
    "AgentConnector",
    "AgentRegistry",
    "AgentManager",
    "SmartAgentMatcher",
    "CommandIntent",
    "AgentCapabilities",
    "TaskManager",
    "FounderApproval",
    "FounderApprovalExecutor",
    "ApprovalDatabase",
    "ApprovalQueue",
    "ApprovalControl",
    "UdaanDatabase",
    "UdaanMemory",
    "UdaanHistory",
    "ExecutionLogs",
    "AgentResult",
    "GeminiBrain",
    "UdaanSecurity",
    "UdaanStatus",
    "UdaanAPI",
    "UdaanCommandCenter",
    "VideoPreview",
    "VideoApprovalController",
    "VideoShareController",
    "AndroidShareBridge"
]


AGENT_MODULES = [
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
]


def check_module(module_name):

    result = {
        "module": module_name,
        "status": "UNKNOWN",
        "message": ""
    }

    try:

        module = importlib.import_module(module_name)

        result["status"] = "ONLINE"
        result["message"] = "Import successful."

        functions = []

        for name in dir(module):

            if name.startswith("_"):
                continue

            try:
                value = getattr(module, name)

                if callable(value):
                    functions.append(name)

            except Exception:
                pass

        result["functions"] = functions

        return result

    except Exception as error:

        result["status"] = "ERROR"
        result["message"] = str(error)
        result["functions"] = []

        return result


def run_audit():

    print()
    print("=" * 65)
    print("          UDAAN AI — PYTHON CORE AUDIT")
    print("=" * 65)

    print()
    print("🧠 CORE MODULES")
    print("-" * 65)

    core_online = 0
    core_error = 0

    for module_name in CORE_MODULES:

        result = check_module(module_name)

        if result["status"] == "ONLINE":

            core_online += 1

            print(
                f"✅ {module_name:<32} ONLINE"
            )

        else:

            core_error += 1

            print(
                f"❌ {module_name:<32} ERROR"
            )

            print(
                f"   └─ {result['message']}"
            )

    print()
    print("🤖 AI AGENTS")
    print("-" * 65)

    agent_online = 0
    agent_error = 0

    for module_name in AGENT_MODULES:

        result = check_module(module_name)

        if result["status"] == "ONLINE":

            agent_online += 1

            print(
                f"✅ {module_name:<32} ONLINE"
            )

        else:

            agent_error += 1

            print(
                f"❌ {module_name:<32} ERROR"
            )

            print(
                f"   └─ {result['message']}"
            )

    total = (
        len(CORE_MODULES)
        + len(AGENT_MODULES)
    )

    online = core_online + agent_online
    errors = core_error + agent_error

    print()
    print("=" * 65)
    print("                 AUDIT SUMMARY")
    print("=" * 65)

    print()
    print("Total modules :", total)
    print("Online        :", online)
    print("Errors        :", errors)

    if errors == 0:

        print()
        print("🟢 PYTHON CORE STRUCTURE: HEALTHY")

    else:

        print()
        print("🟡 PYTHON CORE STRUCTURE: NEEDS FIXES")

    report = {
        "audit_time": datetime.now().isoformat(),
        "total_modules": total,
        "online": online,
        "errors": errors,
        "core_online": core_online,
        "core_errors": core_error,
        "agents_online": agent_online,
        "agents_errors": agent_error
    }

    try:

        with open(
            "udaan_python_audit.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "UDAAN AI PYTHON CORE AUDIT\n"
            )

            file.write(
                "=" * 50 + "\n"
            )

            for key, value in report.items():

                file.write(
                    f"{key}: {value}\n"
                )

        print()
        print(
            "📄 Report saved: "
            "udaan_python_audit.txt"
        )

    except Exception as error:

        print()
        print(
            "⚠️ Report save failed:",
            error
        )

    print()
    print("=" * 65)


if __name__ == "__main__":

    run_audit()