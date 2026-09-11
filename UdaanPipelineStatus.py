Step 130 — File name: UdaanPipelineStatus.py

# ==========================================
# UDAAN AI - PIPELINE STATUS
# STEP 130
# ==========================================

from UdaanAutomationController import (
    run_automation_cycle,
    run_approved_upload_cycle
)


def get_pipeline_status():

    return {
        "status": "ONLINE",
        "system": "UDAAN AI",
        "modules": {
            "research": "READY",
            "content_strategy": "READY",
            "video_pipeline": "READY",
            "founder_approval": "ENABLED",
            "upload_scheduler": "READY",
            "youtube_upload": "READY",
            "automation": "READY"
        }
    }


def start_content_cycle(
    channel=None,
    max_results=5
):

    return run_automation_cycle(
        channel=channel,
        max_results=max_results
    )


def start_approved_upload():

    return run_approved_upload_cycle()
