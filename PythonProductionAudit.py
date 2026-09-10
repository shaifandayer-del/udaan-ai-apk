# PythonProductionAudit.py

import importlib
import inspect
import os
import sqlite3


CORE_MODULES = [
    "UdaanCore",
    "AgentConnector",
    "AgentResult",
    "TaskManager",
    "FounderApproval",
    "ApprovalDatabase",
    "UdaanMemory",
    "GeminiBrain",
    "UdaanSecurity",
    "ExecutionLogs",
    "UdaanAPI",
    "UdaanStatus"
]


AGENTS = [
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


VIDEO_MODULES = [
    "VideoPreview",
    "VideoApprovalController",
    "VideoShareController",
    "AndroidShareBridge",
    "YouTubeUploader",
    "YouTubeOAuth"
]


REQUIRED_FUNCTIONS = {
    "UdaanCore": ["process_command"],
    "AgentConnector": ["run_agent"],
    "SmartAgentMatcher": ["match_agent"],
    "TaskManager": ["create_task"],
    "FounderApproval": ["request_approval", "approve", "reject"],
    "ApprovalDatabase": ["save_approval"],
    "UdaanMemory": ["save_memory"],
    "GeminiBrain": ["ask_gemini"],
    "ExecutionLogs": ["show_logs"],
    "UdaanAPI": ["api_status", "handle_command"],
    "UdaanStatus": [
        "health_check",
        "get_status",
        "system_status"
    ],
    "VideoPreview": ["create_preview"],
    "VideoApprovalController": [
        "create_video_preview",
        "get_video_preview",
        "approve_video",
        "reject_video"
    ],
    "VideoShareController": ["prepare_video_share"],
    "AndroidShareBridge": ["prepare_video_share"]
}


def check_module(module_name):

    try:
        module = importlib.import_module(module_name)
        return True, module, ""

    except Exception as e:
        return False, None, str(e)


def check_functions(module_name, module):

    required = REQUIRED_FUNCTIONS.get(
        module_name,
        []
    )

    missing = []

    for function_name in required:

        function = getattr(
            module,
            function_name,
            None
        )

        if not callable(function):
            missing.append(function_name)

    return missing


def check_database():

    db_names = [
        "udaan.db",
        "udaan_ai.db"
    ]

    found_db = None

    for db in db_names:

        if os.path.exists(db):
            found_db = db
            break

    if not found_db:
        return False, "Database file not found"

    try:

        connection = sqlite3.connect(
            found_db
        )

        cursor = connection.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table'"
        )

        tables = [
            row[0]
            for row in cursor.fetchall()
        ]

        connection.close()

        return True, (
            f"{found_db} | "
            f"{len(tables)} tables"
        )

    except Exception as e:

        return False, str(e)


def audit_group(title, modules):

    print()
    print("-" * 65)
    print(title)
    print("-" * 65)

    passed = 0

    for module_name in modules:

        success, module, error = check_module(
            module_name
        )

        if not success:

            print(
                f"🔴 {module_name:<30} ERROR"
            )

            print(
                f"   → {error}"
            )

            continue

        missing = check_functions(
            module_name,
            module
        )

        if missing:

            print(
                f"🟡 {module_name:<30} "
                f"MISSING"
            )

            print(
                "   → " +
                ", ".join(missing)
            )

        else:

            print(
                f"🟢 {module_name:<30} ONLINE"
            )

            passed += 1

    return passed


def main():

    print()
    print("=" * 65)
    print("        UDAAN AI — PRODUCTION READINESS AUDIT")
    print("=" * 65)

    total = 0
    passed = 0

    # Core
    core_passed = audit_group(
        "🧠 CORE SYSTEM",
        CORE_MODULES
    )

    total += len(CORE_MODULES)
    passed += core_passed

    # Agents
    agent_passed = audit_group(
        "🤖 AI AGENTS",
        AGENTS
    )

    total += len(AGENTS)
    passed += agent_passed

    # Video
    video_passed = audit_group(
        "🎬 VIDEO SYSTEM",
        VIDEO_MODULES
    )

    total += len(VIDEO_MODULES)
    passed += video_passed

    # Database
    print()
    print("-" * 65)
    print("🗄️ DATABASE")
    print("-" * 65)

    db_ok, db_message = check_database()

    if db_ok:
        print("🟢 Database".ljust(35), "ONLINE")
        print("   →", db_message)
        passed += 1
    else:
        print("🔴 Database".ljust(35), "ERROR")
        print("   →", db_message)

    total += 1

    # Final
    percentage = int(
        (passed / total) * 100
    )

    print()
    print("=" * 65)
    print(
        f"PRODUCTION AUDIT: "
        f"{passed}/{total} PASS"
    )
    print(
        f"READINESS SCORE: {percentage}%"
    )
    print("=" * 65)

    if percentage == 100:

        print()
        print("🚀 PYTHON PRODUCTION AUDIT PASSED")
        print("🟢 PYTHON CORE IS READY FOR FINALIZATION")

    elif percentage >= 90:

        print()
        print("🟡 ALMOST READY")
        print("Some components still need attention.")

    else:

        print()
        print("🔴 NOT READY")
        print("Fix the reported components first.")

    print("=" * 65)
    print()


if __name__ == "__main__":
    main()