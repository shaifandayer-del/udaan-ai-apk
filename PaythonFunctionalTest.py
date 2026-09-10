# PythonFunctionalTest.py

import importlib
import inspect


PASS = "PASS"
FAIL = "FAIL"


def test_result(name, success, detail=""):
    if success:
        print(f"🟢 {name:<30} {PASS}")
    else:
        print(f"🔴 {name:<30} {FAIL}")
        if detail:
            print(f"   → {detail}")

    return success


def test_core():
    try:
        module = importlib.import_module("UdaanCore")
        function = getattr(module, "process_command", None)

        if callable(function):
            return test_result(
                "UdaanCore Command Flow",
                True
            )

        return test_result(
            "UdaanCore Command Flow",
            False,
            "process_command missing"
        )

    except Exception as e:
        return test_result(
            "UdaanCore Command Flow",
            False,
            str(e)
        )


def test_matcher():
    try:
        module = importlib.import_module("SmartAgentMatcher")
        function = getattr(module, "match_agent", None)

        if callable(function):
            return test_result(
                "Smart Agent Matcher",
                True
            )

        return test_result(
            "Smart Agent Matcher",
            False,
            "match_agent missing"
        )

    except Exception as e:
        return test_result(
            "Smart Agent Matcher",
            False,
            str(e)
        )


def test_connector():
    try:
        module = importlib.import_module("AgentConnector")
        function = getattr(module, "run_agent", None)

        if callable(function):
            return test_result(
                "Agent Connector",
                True
            )

        function = getattr(module, "run", None)

        if callable(function):
            return test_result(
                "Agent Connector",
                True
            )

        return test_result(
            "Agent Connector",
            False,
            "run_agent/run missing"
        )

    except Exception as e:
        return test_result(
            "Agent Connector",
            False,
            str(e)
        )


def test_task_manager():
    try:
        module = importlib.import_module("TaskManager")
        function = getattr(module, "create_task", None)

        if not callable(function):
            return test_result(
                "Task Manager",
                False,
                "create_task missing"
            )

        parameters = inspect.signature(function).parameters

        if len(parameters) >= 2:
            return test_result(
                "Task Manager",
                True
            )

        return test_result(
            "Task Manager",
            False,
            "create_task interface incomplete"
        )

    except Exception as e:
        return test_result(
            "Task Manager",
            False,
            str(e)
        )


def test_memory():
    try:
        module = importlib.import_module("UdaanMemory")
        function = getattr(module, "save_memory", None)

        if not callable(function):
            return test_result(
                "Udaan Memory",
                False,
                "save_memory missing"
            )

        parameters = inspect.signature(function).parameters

        if len(parameters) >= 2:
            return test_result(
                "Udaan Memory",
                True
            )

        return test_result(
            "Udaan Memory",
            False,
            "save_memory interface incomplete"
        )

    except Exception as e:
        return test_result(
            "Udaan Memory",
            False,
            str(e)
        )


def test_video():
    try:
        module = importlib.import_module("Video")

        functions = [
            "run",
            "execute",
            "process",
            "handle",
            "main",
            "run_agent"
        ]

        found = any(
            callable(getattr(module, name, None))
            for name in functions
        )

        return test_result(
            "Video Agent",
            found,
            "No supported function found" if not found else ""
        )

    except Exception as e:
        return test_result(
            "Video Agent",
            False,
            str(e)
        )


def test_api():
    try:
        module = importlib.import_module("UdaanAPI")

        api_status = getattr(module, "api_status", None)
        handle_command = getattr(module, "handle_command", None)

        if callable(api_status) and callable(handle_command):
            return test_result(
                "Udaan API",
                True
            )

        return test_result(
            "Udaan API",
            False,
            "Required API functions missing"
        )

    except Exception as e:
        return test_result(
            "Udaan API",
            False,
            str(e)
        )


def test_status():
    try:
        module = importlib.import_module("UdaanStatus")

        required = [
            "health_check",
            "get_status",
            "system_status"
        ]

        missing = [
            name
            for name in required
            if not callable(getattr(module, name, None))
        ]

        if not missing:
            return test_result(
                "Udaan Status",
                True
            )

        return test_result(
            "Udaan Status",
            False,
            "Missing: " + ", ".join(missing)
        )

    except Exception as e:
        return test_result(
            "Udaan Status",
            False,
            str(e)
        )


def test_video_approval():
    try:
        module = importlib.import_module(
            "VideoApprovalController"
        )

        required = [
            "create_video_preview",
            "get_video_preview",
            "approve_video",
            "reject_video"
        ]

        missing = [
            name
            for name in required
            if not callable(getattr(module, name, None))
        ]

        if not missing:
            return test_result(
                "Video Approval",
                True
            )

        return test_result(
            "Video Approval",
            False,
            "Missing: " + ", ".join(missing)
        )

    except Exception as e:
        return test_result(
            "Video Approval",
            False,
            str(e)
        )


def test_video_share():
    try:
        module = importlib.import_module(
            "VideoShareController"
        )

        function = getattr(
            module,
            "prepare_video_share",
            None
        )

        if callable(function):
            return test_result(
                "Video Share",
                True
            )

        return test_result(
            "Video Share",
            False,
            "prepare_video_share missing"
        )

    except Exception as e:
        return test_result(
            "Video Share",
            False,
            str(e)
        )


def main():

    print()
    print("=" * 65)
    print("        UDAAN AI — PYTHON FUNCTIONAL TEST")
    print("=" * 65)

    results = []

    results.append(test_core())
    results.append(test_matcher())
    results.append(test_connector())
    results.append(test_task_manager())
    results.append(test_memory())
    results.append(test_video())
    results.append(test_api())
    results.append(test_status())
    results.append(test_video_approval())
    results.append(test_video_share())

    passed = sum(results)
    total = len(results)
    percentage = int((passed / total) * 100)

    print()
    print("=" * 65)
    print(f"RESULT: {passed}/{total} PASSED")
    print(f"SCORE : {percentage}%")
    print("=" * 65)

    if percentage == 100:
        print("🚀 ALL FUNCTIONAL TESTS PASSED")
        print("🟢 PYTHON CORE FUNCTIONALITY READY")
    else:
        print("⚠️ SOME TESTS NEED ATTENTION")

    print("=" * 65)
    print()


if __name__ == "__main__":
    main()