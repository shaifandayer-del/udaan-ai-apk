# ==========================================
# UDAAN AI - PRODUCTION PIPELINE
# STEP 128
# ==========================================

from ContentVideoOrchestrator import create_content_videos
from VideoProductionPipeline import (
    prepare_video_file,
    mark_preview_ready,
    request_video_approval
)
from UploadScheduler import schedule_daily


def run_production_pipeline(
    channel=None,
    max_results=5,
    upload_hour=18,
    upload_minute=0
):

    content_result = create_content_videos(
        channel=channel,
        max_results=max_results
    )

    if content_result.get("status") != "SUCCESS":
        return content_result

    processed = []

    for item in content_result.get(
        "pipeline",
        []
    ):

        video_data = item.get(
            "video_job",
            {}
        )

        job = video_data.get(
            "job",
            {}
        )

        job_id = job.get("job_id")

        if not job_id:
            continue

        prepared = prepare_video_file(
            job_id
        )

        if prepared.get("status") != "SUCCESS":
            continue

        preview = mark_preview_ready(
            job_id
        )

        if preview.get("status") != "SUCCESS":
            continue

        approval = request_video_approval(
            job_id
        )

        if approval.get("status") != "PENDING_APPROVAL":
            continue

        scheduled = schedule_daily(
            video_path=prepared.get(
                "video_path"
            ),
            channel=job.get("channel") or channel,
            hour=upload_hour,
            minute=upload_minute,
            title=job.get(
                "topic",
                "UDAAN AI Video"
            ),
            description=(
                "Created by UDAAN AI."
            )
        )

        processed.append({
            "job_id": job_id,
            "research":
                item.get("research"),
            "strategy":
                item.get("strategy"),
            "video":
                prepared,
            "preview":
                preview,
            "approval":
                approval,
            "schedule":
                scheduled
        })

    return {
        "status": "SUCCESS",
        "agent": "UDAAN Production Pipeline",
        "total_processed": len(processed),
        "pipeline": processed
    }


def run_pipeline(
    channel=None,
    max_results=5
):

    return run_production_pipeline(
        channel=channel,
        max_results=max_results
    )
