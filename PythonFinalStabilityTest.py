# PythonFinalStabilityTest.py

import importlib
import os
import sqlite3


CORE = [
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

VIDEO = [
    "VideoPreview",
    "VideoApprovalController",
    "VideoShareController",
    "AndroidShareBridge"
]

REQUIRED = {
    "UdaanCore": ["process_command"],
    "AgentConnector": ["run_agent"],
    "TaskManager": ["create_task"],
    "FounderApproval": [
        "request_approval",
        "approve",
        "reject"
    ],
    "UdaanMemory": ["save_memory"],
    "GeminiBrain": ["ask_gemini"],
    "UdaanAPI": [
        "api_status",
        "handle_command"
    ],
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
    "VideoShareController": [
        "prepare_video_share"
    ],
    "AndroidShareBridge": [
        "prepare_video_share"
    ]
}


def fresh_import(name):
    try:
        importlib.invalidate_caches()

        if name in importlib.sys.modules:
            del importlib.sys.modules[name]

        return importlib.import_module(name), None

    except Exception as e:
        return None, str(e)


def check_group(title, modules):

    print()
    print("-" * 65)
    print(title)
    print("-" * 65)

    passed = 0

    for name in modules:

        module, error = fresh_import(name)

        if module is None:
            print(f"🔴 {name:<32} FAIL")
            print(f"   → {error}")
            continue

        missing = []

        for function_name in REQUIRED.get(name, []):

            function = getattr(
                module,
                function_name,
                None
            )

            if not callable(function):
                missing.append(function_name)

        if missing:

            print(f"🟡 {name:<32} FAIL")
            print(
                "   → Missing: "
                + ", ".join(missing)
            )

        else:

            print(f"🟢 {name:<32} PASS")
            passed += 1

    return passed


def check_database():

    print()
    print("-" * 65)
    print("DATABASE STABILITY")
    print("-" * 65)

    databases = [
        "udaan.db",
        "udaan_ai.db"
    ]

    for db in databases:

        if not os.path.exists(db):
            continue

        try:

            connection = sqlite3.connect(db)
            cursor = connection.cursor()

            cursor.execute(
                "SELECT name "
                "FROM sqlite_master "
                "WHERE type='table'"
            )

            tables = cursor.fetchall()

            connection.close()

            print("🟢 Database PASS")
            print(f"   → {db}")
            print(f"   → Tables: {len(tables)}")

            return True

        except Exception as e:

            print("🔴 Database FAIL")
            print("   →", e)

            return False

    print("🟡 Database WARNING")
    print("   → No database file found")

    return False


def main():

    print()
    print("=" * 65)
    print("       UDAAN AI — FINAL STABILITY TEST")
    print("=" * 65)

    total = 0
    passed = 0

    core_passed = check_group(
        "🧠 CORE SYSTEM",
        CORE
    )

    total += len(CORE)
    passed += core_passed

    agent_passed = check_group(
        "🤖 AI AGENTS",
        AGENTS
    )

    total += len(AGENTS)
    passed += agent_passed

    video_passed = check_group(
        "🎬 VIDEO SYSTEM",
        VIDEO
    )

    total += len(VIDEO)
    passed += video_passed

    database_ok = check_database()

    total += 1

    if database_ok:
        passed += 1

    percentage = int(
        (passed / total) * 100
    )

    print()
    print("=" * 65)
    print(
        f"FINAL STABILITY: "
        f"{passed}/{total}"
    )
    print(
        f"SCORE: {percentage}%"
    )
    print("=" * 65)

    if percentage == 100:

        print()
        print("🚀 FINAL STABILITY TEST PASSED")
        print("🟢 PYTHON CORE STABLE")
        print("🟢 PYTHON PHASE READY TO CLOSE")

    else:

        print()
        print("⚠️ STABILITY ISSUES FOUND")
        print("🔴 PYTHON PHASE NOT READY TO CLOSE")

    print("=" * 65)
    print()


if __name__ == "__main__":
    main()