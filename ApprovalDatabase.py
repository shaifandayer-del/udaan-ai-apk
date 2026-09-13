import sqlite3
import datetime


DATABASE_FILE = "udaan.db"


class ApprovalDatabase:
    def __init__(self, database_file=DATABASE_FILE):
        self.database_file = database_file
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(
            self.database_file
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        connection = self._connect()

        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS approvals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    approval_id TEXT UNIQUE NOT NULL,
                    action TEXT NOT NULL,
                    agent TEXT,
                    platform TEXT,
                    file_path TEXT,
                    title TEXT,
                    description TEXT,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            connection.commit()

        finally:
            connection.close()

    def save(self, approval):
        now = datetime.datetime.now().isoformat()

        connection = self._connect()

        try:
            connection.execute(
                """
                INSERT OR REPLACE INTO approvals
                (
                    approval_id,
                    action,
                    agent,
                    platform,
                    file_path,
                    title,
                    description,
                    status,
                    result,
                    error,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    approval.get("approval_id"),
                    approval.get("action"),
                    approval.get("agent"),
                    approval.get("platform"),
                    approval.get("file_path"),
                    approval.get("title"),
                    approval.get("description"),
                    approval.get("status", "PENDING"),
                    str(approval.get("result"))
                    if approval.get("result") is not None
                    else None,
                    str(approval.get("error"))
                    if approval.get("error") is not None
                    else None,
                    approval.get("created_at", now),
                    now
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get(self, approval_id):
        connection = self._connect()

        try:
            row = connection.execute(
                """
                SELECT *
                FROM approvals
                WHERE approval_id = ?
                """,
                (approval_id,)
            ).fetchone()

            return dict(row) if row else None

        finally:
            connection.close()

    def get_pending(self):
        connection = self._connect()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM approvals
                WHERE status = 'PENDING'
                ORDER BY id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()

    def get_all(self, limit=100):
        connection = self._connect()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM approvals
                ORDER BY id DESC
                LIMIT ?
                """,
                (int(limit),)
            ).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()

    def update_status(
        self,
        approval_id,
        status,
        result=None,
        error=None
    ):
        now = datetime.datetime.now().isoformat()

        connection = self._connect()

        try:
            connection.execute(
                """
                UPDATE approvals
                SET status = ?,
                    result = ?,
                    error = ?,
                    updated_at = ?
                WHERE approval_id = ?
                """,
                (
                    status,
                    str(result)
                    if result is not None
                    else None,
                    str(error)
                    if error is not None
                    else None,
                    now,
                    approval_id
                )
            )

            connection.commit()

        finally:
            connection.close()

    def delete(self, approval_id):
        connection = self._connect()

        try:
            connection.execute(
                """
                DELETE FROM approvals
                WHERE approval_id = ?
                """,
                (approval_id,)
            )

            connection.commit()

        finally:
            connection.close()


approval_database = ApprovalDatabase()


def save_approval(approval):
    return approval_database.save(approval)


def get_approval(approval_id):
    return approval_database.get(
        approval_id
    )


def get_pending_approvals():
    return approval_database.get_pending()


def get_all_approvals(limit=100):
    return approval_database.get_all(limit)


def update_approval_status(
    approval_id,
    status,
    result=None,
    error=None
):
    return approval_database.update_status(
        approval_id,
        status,
        result,
        error
    )


def delete_approval(approval_id):
    return approval_database.delete(
        approval_id
    )
