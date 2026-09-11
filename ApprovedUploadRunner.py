# ==========================================
# UDAAN AI - APPROVED UPLOAD RUNNER
# STEP 126
# ==========================================

from UploadScheduler import get_approved_schedules
from YouTubePublishEngine import publish_video


class ApprovedUploadRunner:

    def run(self):

        schedules = get_approved_schedules()
        results = []

        for schedule in schedules:

            video_path = schedule.get("video_path")
            title = schedule.get("title") or "UDAAN AI Video"
            description = schedule.get("description") or ""

            if not video_path:
                results.append({
                    "status": "FAILED",
                    "schedule_id": schedule.get("schedule_id"),
                    "message": "Video path missing."
                })
                continue

            result = publish_video(
                video_path=video_path,
                title=title,
                description=description,
                privacy_status="private"
            )

            results.append({
                "schedule_id": schedule.get("schedule_id"),
                "channel": schedule.get("channel"),
                "upload": result
            })

        return {
            "status": "SUCCESS",
            "total": len(results),
            "results": results
        }


_runner = ApprovedUploadRunner()


def run_approved_uploads():

    return _runner.run()
