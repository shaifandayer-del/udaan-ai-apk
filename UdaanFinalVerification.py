# ==========================================
# UDAAN AI - FINAL VERIFICATION
# STEP 138
# ==========================================

import importlib


REQUIRED_MODULES = [
    "UdaanFinalIntegration",
    "UdaanAutomationController",
    "UdaanProductionPipeline",
    "ContentVideoOrchestrator",
    "ContentStrategyEngine",
    "VideoProductionPipeline",
    "ActualVideoRenderer",
    "YouTubePublishEngine",
    "YouTubeOAuthManager",
    "MultiChannelAuthManager",
    "InstagramPublishEngine",
    "PersistentUploadScheduler",
    "UdaanNotificationManager",
    "FounderApproval",
    "FounderApprovalExecutor",
    "UdaanAPI"
]


def verify_modules():

    results = {}

    for module_name in REQUIRED_MODULES:

        try:
            importlib.import_module(module_name)
            results[module_name] = "READY"

        except Exception as error:

            results[module_name] = {
                "status": "ERROR",
                "error": str(error)
            }

    failed = [
        name
        for name, result in results.items()
        if result != "READY"
    ]

    return {
        "status": "SUCCESS" if not failed else "FAILED",
        "total_modules": len(REQUIRED_MODULES),
        "ready_modules": len(REQUIRED_MODULES) - len(failed),
        "failed_modules": failed,
        "modules": results
    }


def verify_environment():

    import os

    checks = {
        "python": True,
        "youtube_api_key": bool(
            os.environ.get("YOUTUBE_API_KEY")
        ),
        "youtube_access_token": bool(
            os.environ.get("YOUTUBE_ACCESS_TOKEN")
        ),
        "instagram_access_token": bool(
            os.environ.get("INSTAGRAM_ACCESS_TOKEN")
        ),
        "instagram_account_id": bool(
            os.environ.get("INSTAGRAM_ACCOUNT_ID")
        ),
        "founder_api_key": bool(
            os.environ.get("UDAAN_FOUNDER_API_KEY")
        )
    }

    return {
        "status": "READY",
        "checks": checks
    }


def run_final_verification():

    module_result = verify_modules()
    environment_result = verify_environment()

    overall_status = (
        "READY"
        if module_result["status"] == "SUCCESS"
        else "FAILED"
    )

    return {
        "system": "UDAAN AI",
        "status": overall_status,
        "module_verification": module_result,
        "environment_verification": environment_result
    }


if __name__ == "__main__":

    result = run_final_verification()

    print("=" * 60)
    print("          UDAAN AI FINAL VERIFICATION")
    print("=" * 60)

    print(
        "STATUS :",
        result["status"]
    )

    print(
        "MODULES:",
        result["module_verification"]["ready_modules"],
        "/",
        result["module_verification"]["total_modules"]
    )

    if result["module_verification"]["failed_modules"]:

        print()
        print("FAILED MODULES:")

        for module in result[
            "module_verification"
        ]["failed_modules"]:

            print("-", module)

    print("=" * 60)
