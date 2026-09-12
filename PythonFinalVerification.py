import importlib
import os


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


def verify_module(name):
    try:
        importlib.import_module(name)
        return {
            "module": name,
            "status": "PASS",
            "error": None
        }
    except Exception as error:
        return {
            "module": name,
            "status": "FAIL",
            "error": f"{type(error).__name__}: {error}"
        }


def verify_agent(name):
    try:
        from AgentConnector import run_agent

        result = run_agent(
            name,
            "UDAAN AI final verification"
        )

        if not isinstance(result, dict):
            return {
                "agent": name,
                "status": "FAIL",
                "error": "Invalid agent response."
            }

        return {
            "agent": name,
            "status": result.get("status", "UNKNOWN"),
            "message": result.get("message", ""),
            "error": result.get("error")
        }

    except Exception as error:
        return {
            "agent": name,
            "status": "FAIL",
            "error": f"{type(error).__name__}: {error}"
        }


def verify_environment():
    return {
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "founder_api": bool(os.getenv("UDAAN_FOUNDER_API_KEY")),
        "youtube": bool(
            os.getenv("YOUTUBE_CLIENT_JSON")
            or os.getenv("YOUTUBE_TOKEN_JSON")
        ),
        "instagram": bool(
            os.getenv("INSTAGRAM_ACCESS_TOKEN")
            or os.getenv("META_ACCESS_TOKEN")
        )
    }


def verify():
    modules = [
        verify_module(name)
        for name in CORE_MODULES
    ]

    agents = [
        verify_agent(name)
        for name in AGENTS
    ]

    module_failures = [
        item for item in modules
        if item["status"] == "FAIL"
    ]

    agent_failures = [
        item for item in agents
        if item["status"] in ("FAIL", "FAILED")
    ]

    return {
        "status": "PASS"
        if not module_failures and not agent_failures
        else "FAIL",
        "environment": verify_environment(),
        "modules": modules,
        "agents": agents,
        "module_failures": len(module_failures),
        "agent_failures": len(agent_failures)
    }


def main():
    result = verify()

    print("=" * 45)
    print("UDAAN AI FINAL PYTHON VERIFICATION")
    print("=" * 45)

    print(f"STATUS: {result['status']}")
    print(f"Module Failures: {result['module_failures']}")
    print(f"Agent Failures: {result['agent_failures']}")

    if result["status"] == "PASS":
        print("UDAAN AI FINAL VERIFICATION: PASS")
    else:
        print("UDAAN AI FINAL VERIFICATION: FAIL")

    return result


def run(command=""):
    return verify()


def execute(command=""):
    return verify()


def process(command=""):
    return verify()


def handle(command=""):
    return verify()


def run_agent(command=""):
    return verify()


if __name__ == "__main__":
    main()
