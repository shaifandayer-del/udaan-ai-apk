PythonProductionAudit.py

import importlib
import inspect
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


def audit_module(name):
    try:
        module = importlib.import_module(name)

        functions = [
            item
            for item in dir(module)
            if callable(getattr(module, item, None))
            and not item.startswith("_")
        ]

        return {
            "module": name,
            "status": "PASS",
            "functions": functions
        }

    except Exception as error:
        return {
            "module": name,
            "status": "FAIL",
            "error": f"{type(error).__name__}: {error}"
        }


def audit_agent(name):
    try:
        module = importlib.import_module(name)

        required = [
            "run",
            "execute",
            "process",
            "handle",
            "run_agent"
        ]

        available = {
            function: callable(
                getattr(module, function, None)
            )
            for function in required
        }

        missing = [
            function
            for function, available_status in available.items()
            if not available_status
        ]

        return {
            "agent": name,
            "status": "PASS" if not missing else "FAIL",
            "available_functions": available,
            "missing_functions": missing
        }

    except Exception as error:
        return {
            "agent": name,
            "status": "FAIL",
            "error": f"{type(error).__name__}: {error}"
        }


def audit_environment():
    return {
        "python": os.sys.version.split()[0],
        "gemini_api": bool(
            os.getenv("GEMINI_API_KEY")
        ),
        "founder_api": bool(
            os.getenv("UDAAN_FOUNDER_API_KEY")
        ),
        "youtube_oauth": bool(
            os.getenv("YOUTUBE_CLIENT_JSON")
            or os.getenv("YOUTUBE_TOKEN_JSON")
        ),
        "instagram_api": bool(
            os.getenv("INSTAGRAM_ACCESS_TOKEN")
            or os.getenv("META_ACCESS_TOKEN")
        )
    }


def run_audit():
    modules = [
        audit_module(module)
        for module in CORE_MODULES
    ]

    agents = [
        audit_agent(agent)
        for agent in AGENTS
    ]

    failures = [
        item
        for item in modules + agents
        if item.get("status") == "FAIL"
    ]

    return {
        "status": "PASS" if not failures else "FAIL",
        "environment": audit_environment(),
        "core_modules": modules,
        "agents": agents,
        "failures": len(failures)
    }


def main():
    result = run_audit()

    print("=" * 50)
    print("UDAAN AI PYTHON PRODUCTION AUDIT")
    print("=" * 50)
    print(f"STATUS: {result['status']}")
    print(f"FAILURES: {result['failures']}")

    for item in result["core_modules"]:
        print(
            f"MODULE: {item['module']} "
            f"-> {item['status']}"
        )

    for item in result["agents"]:
        print(
            f"AGENT: {item['agent']} "
            f"-> {item['status']}"
        )

    return result


def run(command=""):
    return run_audit()


def execute(command=""):
    return run_audit()


def process(command=""):
    return run_audit()


def handle(command=""):
    return run_audit()


def run_agent(command=""):
    return run_audit()


if __name__ == "__main__":
    main()
