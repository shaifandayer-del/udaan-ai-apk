# ==========================================
# UDAAN AI - MULTI CHANNEL UPLOAD SCHEDULER
# STEP 122
# ==========================================

from datetime import datetime, timedelta


class UploadScheduler:

    def __init__(self):
        self.schedules = []

    def timestamp(self):
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def schedule_upload(
        self,
        video_path,
        channel,
        upload_time,
        title=None,
        description=None
    ):

        if not video_path:
            return {
                "status": "FAILED",
                "message": "Video path missing."
            }

        if not channel:
            return {
                "status": "FAILED",
                "message": "Channel missing."
            }

        schedule = {
            "schedule_id":
                "SCH-" + datetime.now().strftime(
                    "%Y%m%d%H%M%S%f"
                ),
            "video_path": video_path,
            "channel": channel,
            "upload_time": str(upload_time),
            "title": title,
            "description": description,
            "status": "WAITING",
            "founder_approval_required": True,
            "created_at": self.timestamp()
        }

        self.schedules.append(schedule)

        return {
            "status": "SUCCESS",
            "schedule": schedule
        }

    def schedule_daily(
        self,
        video_path,
        channel,
        hour=18,
        minute=0,
        title=None,
        description=None
    ):

        upload_time = (
            datetime.now()
            .replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )
        )

        if upload_time <= datetime.now():
            upload_time += timedelta(days=1)

        return self.schedule_upload(
            video_path=video_path,
            channel=channel,
            upload_time=upload_time.isoformat(),
            title=title,
            description=description
        )

    def approve_schedule(
        self,
        schedule_id
    ):

        for schedule in self.schedules:

            if schedule["schedule_id"] == schedule_id:

                schedule["status"] = (
                    "APPROVED_FOR_UPLOAD"
                )

                return {
                    "status": "SUCCESS",
                    "schedule": schedule
                }

        return {
            "status": "FAILED",
            "message": "Schedule not found."
        }

    def cancel_schedule(
        self,
        schedule_id
    ):

        for schedule in self.schedules:

            if schedule["schedule_id"] == schedule_id:

                schedule["status"] = "CANCELLED"

                return {
                    "status": "SUCCESS",
                    "schedule": schedule
                }

        return {
            "status": "FAILED",
            "message": "Schedule not found."
        }

    def get_pending(self):

        return [
            schedule
            for schedule in self.schedules
            if schedule["status"] == "WAITING"
        ]

    def get_approved(self):

        return [
            schedule
            for schedule in self.schedules
            if schedule["status"]
            == "APPROVED_FOR_UPLOAD"
        ]

    def list_schedules(self):

        return {
            "status": "SUCCESS",
            "total": len(self.schedules),
            "schedules": self.schedules
        }


_scheduler = UploadScheduler()


def schedule_upload(
    video_path,
    channel,
    upload_time,
    title=None,
    description=None
):

    return _scheduler.schedule_upload(
        video_path,
        channel,
        upload_time,
        title,
        description
    )


def schedule_daily(
    video_path,
    channel,
    hour=18,
    minute=0,
    title=None,
    description=None
):

    return _scheduler.schedule_daily(
        video_path,
        channel,
        hour,
        minute,
        title,
        description
    )


def approve_schedule(schedule_id):

    return _scheduler.approve_schedule(
        schedule_id
    )


def cancel_schedule(schedule_id):

    return _scheduler.cancel_schedule(
        schedule_id
    )


def get_pending_schedules():

    return _scheduler.get_pending()


def get_approved_schedules():

    return _scheduler.get_approved()


def list_schedules():

    return _scheduler.list_schedules()
