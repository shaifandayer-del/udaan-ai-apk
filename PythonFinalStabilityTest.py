PythonFinalStabilityTest.py

import importlib
import os
import sys


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

CORE_MODULES = [
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
    "UdaanFinalIntegration",
]


def check_module(name):
    try:
        module = importlib.import_module(name)
        return {
            "module": name,
            "status": "PASS",
            "error": None,
            "loaded": module is not None,
        }
    except Exception as error:
        return {
            "module": name,
            "status": "FAIL",
            "error": f"{type(error).__name__}: {error}",
            "loaded": False,
        }


def check_agent(agent):
    try:
        from AgentConnector import run_agent

        result = run_agent(
            agent,
            "UDAAN AI stability test"
        )

        if not isinstance(result, dict):
            return {
                "agent": agent,
                "status": "FAIL",
                "error": "Agent response dictionary nahi hai."
            }

        return {
            "agent": agent,
            "status": result.get("status", "UNKNOWN"),
            "message": result.get("message", ""),
            "error": result.get("error"),
        }

    except Exception as error:
        return {
            "agent": agent,
            "status": "FAIL",
            "error": f"{type(error).__name__}: {error}"
        }


def check_environment():
    return {
        "python_version": sys.version.split()[0],
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        ),
        "youtube_configured": bool(
            os.getenv("YOUTUBE_CLIENT_JSON")
            or os.getenv("YOUTUBE_TOKEN_JSON")
        ),
        "instagram_configured": bool(
            os.getenv("INSTAGRAM_ACCESS_TOKEN")
            or os.getenv("META_ACCESS_TOKEN")
        ),
    }


def run_stability_test():
    core_results = [
        check_module(module)
        for module in CORE_MODULES
    ]

    agent_results = [
        check_agent(agent)
        for agent in AGENTS
    ]

    core_failed = [
        item
        for item in core_results
        if item["status"] == "FAIL"
    ]

    agent_failed = [
        item
        for item in agent_results
        if item["status"] == "FAILED"
        or item["status"] == "FAIL"
    ]

    return {
        "status": "PASS"
        if not core_failed and not agent_failed
        else "FAIL",
        "environment": check_environment(),
        "core_modules": core_results,
        "agents": agent_results,
        "core_failed": len(core_failed),
        "agents_failed": len(agent_failed),
    }


def main():
    print("=" * 40)
    print("UDAAN AI PYTHON FINAL STABILITY TEST")
    print("=" * 40)

    result = run_stability_test()

    print(f"STATUS: {result['status']}")
    print(
        f"Core failures: {result['core_failed']}"
    )
    print(
        f"Agent failures: {result['agents_failed']}"
    )

    if result["status"] == "PASS":
        print("UDAAN AI PYTHON STABILITY: PASS")
    else:
        print("UDAAN AI PYTHON STABILITY: FAIL")

    return result


def run(command=""):
    return run_stability_test()


def execute(command=""):
    return run_stability_test()


def process(command=""):
    return run_stability_test()


def handle(command=""):
    return run_stability_test()


def run_agent(command=""):
    return run_stability_test()


if __name__ == "__main__":
    main()
