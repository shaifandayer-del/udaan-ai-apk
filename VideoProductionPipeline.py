Step 121 — File: VideoProductionPipeline.py

# ==========================================
# UDAAN AI - VIDEO PRODUCTION PIPELINE
# STEP 121
# ==========================================

import os
from datetime import datetime


class VideoProductionPipeline:

    def __init__(self):
        self.output_directory = "udaan_videos"
        self.jobs = []

        os.makedirs(
            self.output_directory,
            exist_ok=True
        )

    def timestamp(self):
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def create_job(
        self,
        topic,
        script=None,
        channel=None,
        duration="60 seconds",
        language="Hindi"
    ):

        topic = str(topic or "").strip()

        if not topic:
            return {
                "status": "FAILED",
                "message": "Video topic empty hai."
            }

        job_id = (
            "VID-"
            + datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            )
        )

        job = {
            "job_id": job_id,
            "topic": topic,
            "script": script,
            "channel": channel,
            "duration": duration,
            "language": language,
            "status": "PREPARING",
            "created_at": self.timestamp(),

            "stages": [
                "SCRIPT",
                "VOICE",
                "VISUALS",
                "SUBTITLES",
                "EDIT",
                "PREVIEW",
                "FOUNDER_APPROVAL",
                "UPLOAD"
            ],

            "approval_required": True,
            "video_path": None
        }

        self.jobs.append(job)

        return {
            "status": "SUCCESS",
            "agent": "Video AI",
            "job": job
        }

    def prepare_video_file(
        self,
        job_id
    ):

        for job in self.jobs:

            if job["job_id"] != job_id:
                continue

            filename = (
                job["job_id"]
                + ".mp4"
            )

            video_path = os.path.join(
                self.output_directory,
                filename
            )

            job["video_path"] = video_path
            job["status"] = "READY_FOR_RENDER"

            return {
                "status": "SUCCESS",
                "job_id": job_id,
                "video_path": video_path,
                "message":
                    "Video production job ready for rendering."
            }

        return {
            "status": "FAILED",
            "message": "Video job not found.",
            "job_id": job_id
        }

    def mark_preview_ready(
        self,
        job_id
    ):

        for job in self.jobs:

            if job["job_id"] == job_id:

                job["status"] = "PREVIEW_READY"

                return {
                    "status": "SUCCESS",
                    "job": job
                }

        return {
            "status": "FAILED",
            "message": "Video job not found."
        }

    def request_founder_approval(
        self,
        job_id
    ):

        for job in self.jobs:

            if job["job_id"] == job_id:

                job["status"] = "WAITING_APPROVAL"

                return {
                    "status": "PENDING_APPROVAL",
                    "job": job,
                    "message":
                        "Founder approval required before upload."
                }

        return {
            "status": "FAILED",
            "message": "Video job not found."
        }

    def approve_upload(
        self,
        job_id
    ):

        for job in self.jobs:

            if job["job_id"] == job_id:

                if job["status"] != "WAITING_APPROVAL":

                    return {
                        "status": "FAILED",
                        "message":
                            "Video is not waiting for approval."
                    }

                job["status"] = "APPROVED_FOR_UPLOAD"

                return {
                    "status": "SUCCESS",
                    "job": job,
                    "message":
                        "Video approved for upload."
                }

        return {
            "status": "FAILED",
            "message": "Video job not found."
        }

    def get_job(
        self,
        job_id
    ):

        for job in self.jobs:

            if job["job_id"] == job_id:
                return {
                    "status": "SUCCESS",
                    "job": job
                }

        return {
            "status": "FAILED",
            "message": "Video job not found."
        }

    def list_jobs(self):

        return {
            "status": "SUCCESS",
            "total_jobs": len(self.jobs),
            "jobs": self.jobs
        }


_pipeline = VideoProductionPipeline()


def create_video_job(
    topic,
    script=None,
    channel=None,
    duration="60 seconds",
    language="Hindi"
):

    return _pipeline.create_job(
        topic,
        script,
        channel,
        duration,
        language
    )


def prepare_video_file(job_id):

    return _pipeline.prepare_video_file(
        job_id
    )


def mark_preview_ready(job_id):

    return _pipeline.mark_preview_ready(
        job_id
    )


def request_video_approval(job_id):

    return _pipeline.request_founder_approval(
        job_id
    )


def approve_video_upload(job_id):

    return _pipeline.approve_upload(
        job_id
    )


def get_video_job(job_id):

    return _pipeline.get_job(
        job_id
    )


def list_video_jobs():

    return _pipeline.list_jobs()
