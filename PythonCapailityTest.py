PythonCapailityTest.py

import importlib
import os


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
    "Creative",
]


def check_module(name):
    try:
        module = importlib.import_module(name)
        return {
            "status": "PASS",
            "module": name,
            "loaded": module is not None
        }
    except Exception as error:
        return {
            "status": "FAIL",
            "module": name,
            "loaded": False,
            "error": f"{type(error).__name__}: {error}"
        }


def check_agent(name):
    try:
        from AgentConnector import run_agent

        result = run_agent(
            name,
            "UDAAN AI capability test"
        )

        if not isinstance(result, dict):
            return {
                "status": "FAIL",
                "agent": name,
                "error": "Invalid response."
            }

        return {
            "status": result.get("status", "UNKNOWN"),
            "agent": name,
            "message": result.get("message", ""),
            "error": result.get("error")
        }

    except Exception as error:
        return {
            "status": "FAIL",
            "agent": name,
            "error": f"{type(error).__name__}: {error}"
        }


def check_environment():
    return {
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "youtube": bool(
            os.getenv("YOUTUBE_CLIENT_JSON")
            or os.getenv("YOUTUBE_TOKEN_JSON")
        ),
        "instagram": bool(
            os.getenv("INSTAGRAM_ACCESS_TOKEN")
            or os.getenv("META_ACCESS_TOKEN")
        ),
        "founder_api": bool(
            os.getenv("UDAAN_FOUNDER_API_KEY")
        )
    }


def run_capability_test():
    modules = [
        check_module(name)
        for name in [
            "GeminiBrain",
            "AgentConnector",
            "Orchestrator",
            "VideoProductionPipeline",
            "ActualVideoRenderer",
            "VideoApprovalController",
            "ApprovedUploadRunner",
            "YouTubePublishEngine",
            "InstagramPublishEngine",
            "MultiChannelAuthManager",
        ]
    ]

    agents = [
        check_agent(agent)
        for agent in AGENTS
    ]

    failures = [
        item
        for item in modules + agents
        if item["status"] in ("FAIL", "FAILED")
    ]

    return {
        "status": "PASS" if not failures else "FAIL",
        "environment": check_environment(),
        "modules": modules,
        "agents": agents,
        "failures": len(failures)
    }


def main():
    result = run_capability_test()

    print("=" * 45)
    print("UDAAN AI PYTHON CAPABILITY TEST")
    print("=" * 45)
    print(f"STATUS: {result['status']}")
    print(f"FAILURES: {result['failures']}")

    return result


def run(command=""):
    return run_capability_test()


def execute(command=""):
    return run_capability_test()


def process(command=""):
    return run_capability_test()


def handle(command=""):
    return run_capability_test()


def run_agent(command=""):
    return run_capability_test()


if __name__ == "__main__":
    main()
