# ==========================================
# UDAAN AI - PERSISTENT UPLOAD SCHEDULER
# STEP 133
# ==========================================

import sqlite3
import os
from datetime import datetime


class PersistentUploadScheduler:

    def __init__(self, database_path="udaan_uploads.db"):
        self.database_path = database_path
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize(self):
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS upload_schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_path TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    channel_id TEXT DEFAULT '',
                    scheduled_at TEXT NOT NULL,
                    status TEXT DEFAULT 'PENDING',
                    created_at TEXT NOT NULL
                )
            """)
            connection.commit()

    def schedule(
        self,
        video_path,
        title,
        scheduled_at,
        description="",
        channel_id=""
    ):

        if not video_path:
            return {
                "status": "FAILED",
                "message": "Video path required."
            }

        now = datetime.now().isoformat()

        with self._connect() as connection:

            cursor = connection.execute(
                """
                INSERT INTO upload_schedule
                (
                    video_path,
                    title,
                    description,
                    channel_id,
                    scheduled_at,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    video_path,
                    title,
                    description,
                    channel_id,
                    scheduled_at,
                    "PENDING",
                    now
                )
            )

            connection.commit()

            return {
                "status": "SUCCESS",
                "schedule_id": cursor.lastrowid,
                "approval_required": True
            }

    def get_pending(self):

        with self._connect() as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT *
                FROM upload_schedule
                WHERE status = 'PENDING'
                ORDER BY scheduled_at ASC
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def approve(self, schedule_id):

        with self._connect() as connection:

            cursor = connection.execute(
                """
                UPDATE upload_schedule
                SET status = 'APPROVED'
                WHERE id = ?
                AND status = 'PENDING'
                """,
                (schedule_id,)
            )

            connection.commit()

            if cursor.rowcount == 0:
                return {
                    "status": "FAILED",
                    "message": "Schedule not found or already processed."
                }

            return {
                "status": "SUCCESS",
                "schedule_id": schedule_id,
                "status_value": "APPROVED"
            }

    def mark_uploaded(self, schedule_id):

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE upload_schedule
                SET status = 'UPLOADED'
                WHERE id = ?
                """,
                (schedule_id,)
            )

            connection.commit()

        return {
            "status": "SUCCESS",
            "schedule_id": schedule_id,
            "status_value": "UPLOADED"
        }

    def cancel(self, schedule_id):

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE upload_schedule
                SET status = 'CANCELLED'
                WHERE id = ?
                """,
                (schedule_id,)
            )

            connection.commit()

        return {
            "status": "SUCCESS",
            "schedule_id": schedule_id,
            "status_value": "CANCELLED"
        }


_scheduler = PersistentUploadScheduler()


def schedule_upload(
    video_path,
    title,
    scheduled_at,
    description="",
    channel_id=""
):

    return _scheduler.schedule(
        video_path,
        title,
        scheduled_at,
        description,
        channel_id
    )


def get_pending_uploads():

    return _scheduler.get_pending()


def approve_upload(schedule_id):

    return _scheduler.approve(
        schedule_id
    )


def mark_uploaded(schedule_id):

    return _scheduler.mark_uploaded(
        schedule_id
    )


def cancel_upload(schedule_id):

    return _scheduler.cancel(
        schedule_id
    )
