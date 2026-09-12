import os
import sys
import importlib


APP_NAME = "UDAAN AI"
APP_VERSION = "1.0.0"
PYTHON_VERSION = sys.version.split()[0]


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


def module_status(module_name):
    try:
        importlib.import_module(module_name)
        return {
            "module": module_name,
            "status": "READY"
        }
    except Exception as error:
        return {
            "module": module_name,
            "status": "FAILED",
            "error": f"{type(error).__name__}: {error}"
        }


def agent_status(agent_name):
    try:
        from AgentConnector import run_agent

        result = run_agent(
            agent_name,
            "UDAAN AI manifest verification"
        )

        return {
            "agent": agent_name,
            "status": result.get("status", "UNKNOWN"),
            "message": result.get("message", ""),
            "error": result.get("error")
        }

    except Exception as error:
        return {
            "agent": agent_name,
            "status": "FAILED",
            "error": f"{type(error).__name__}: {error}"
        }


def environment_status():
    return {
        "python_version": PYTHON_VERSION,
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        ),
        "founder_api_configured": bool(
            os.getenv("UDAAN_FOUNDER_API_KEY")
        ),
        "youtube_configured": bool(
            os.getenv("YOUTUBE_CLIENT_JSON")
            or os.getenv("YOUTUBE_TOKEN_JSON")
        ),
        "instagram_configured": bool(
            os.getenv("INSTAGRAM_ACCESS_TOKEN")
            or os.getenv("META_ACCESS_TOKEN")
        )
    }


def get_manifest():
    modules = [
        module_status(module)
        for module in CORE_MODULES
    ]

    agents = [
        agent_status(agent)
        for agent in AGENTS
    ]

    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "READY",
        "environment": environment_status(),
        "core_modules": modules,
        "agents": agents,
        "agent_count": len(AGENTS)
    }


def verify_manifest():
    manifest = get_manifest()

    module_failures = [
        item for item in manifest["core_modules"]
        if item["status"] == "FAILED"
    ]

    agent_failures = [
        item for item in manifest["agents"]
        if item["status"] in ("FAILED", "FAIL")
    ]

    manifest["status"] = (
        "PASS"
        if not module_failures and not agent_failures
        else "FAIL"
    )

    manifest["module_failures"] = len(module_failures)
    manifest["agent_failures"] = len(agent_failures)

    return manifest


def main():
    result = verify_manifest()

    print("=" * 45)
    print("UDAAN AI PYTHON MANIFEST")
    print("=" * 45)
    print(f"APP: {result['app']}")
    print(f"VERSION: {result['version']}")
    print(f"PYTHON: {PYTHON_VERSION}")
    print(f"AGENTS: {result['agent_count']}")
    print(f"STATUS: {result['status']}")
    print(f"MODULE FAILURES: {result['module_failures']}")
    print(f"AGENT FAILURES: {result['agent_failures']}")

    return result


def run(command=""):
    return verify_manifest()


def execute(command=""):
    return verify_manifest()


def process(command=""):
    return verify_manifest()


def handle(command=""):
    return verify_manifest()


def run_agent(command=""):
    return verify_manifest()


if __name__ == "__main__":
    main()
