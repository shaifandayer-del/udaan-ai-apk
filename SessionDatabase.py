import sqlite3
import datetime


DATABASE_FILE = "udaan_sessions.db"


class SessionDatabase:
    def __init__(self, database_file=DATABASE_FILE):
        self.database_file = database_file
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.database_file)

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    founder TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    closed_at TEXT
                )
                """
            )
            connection.commit()

    def save_session(self, session):
        if not isinstance(session, dict):
            return False

        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO sessions
                (
                    session_id,
                    founder,
                    status,
                    created_at,
                    last_activity,
                    closed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session.get("session_id"),
                    session.get("founder", "Founder"),
                    session.get("status", "ACTIVE"),
                    session.get("created_at"),
                    session.get("last_activity"),
                    session.get("closed_at")
                )
            )
            connection.commit()

        return True

    def get_session(self, session_id):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    session_id,
                    founder,
                    status,
                    created_at,
                    last_activity,
                    closed_at
                FROM sessions
                WHERE session_id = ?
                """,
                (str(session_id),)
            )

            row = cursor.fetchone()

        if not row:
            return None

        return self._row_to_dict(row)

    def update_session(self, session_id, **updates):
        session = self.get_session(session_id)

        if not session:
            return None

        session.update(updates)
        session["last_activity"] = (
            datetime.datetime.now().isoformat()
        )

        self.save_session(session)

        return session

    def close_session(self, session_id):
        now = datetime.datetime.now().isoformat()

        return self.update_session(
            session_id,
            status="CLOSED",
            closed_at=now
        )

    def get_active_sessions(self):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    session_id,
                    founder,
                    status,
                    created_at,
                    last_activity,
                    closed_at
                FROM sessions
                WHERE status = 'ACTIVE'
                ORDER BY created_at DESC
                """
            )

            rows = cursor.fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    def get_all_sessions(self):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    session_id,
                    founder,
                    status,
                    created_at,
                    last_activity,
                    closed_at
                FROM sessions
                ORDER BY created_at DESC
                """
            )

            rows = cursor.fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    def delete_session(self, session_id):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                DELETE FROM sessions
                WHERE session_id = ?
                """,
                (str(session_id),)
            )
            connection.commit()

            return cursor.rowcount > 0

    @staticmethod
    def _row_to_dict(row):
        return {
            "session_id": row[0],
            "founder": row[1],
            "status": row[2],
            "created_at": row[3],
            "last_activity": row[4],
            "closed_at": row[5]
        }


session_database = SessionDatabase()


def save_session(session):
    return session_database.save_session(session)


def get_session(session_id):
    return session_database.get_session(session_id)


def update_session(session_id, **updates):
    return session_database.update_session(
        session_id,
        **updates
    )


def close_session(session_id):
    return session_database.close_session(session_id)


def get_active_sessions():
    return session_database.get_active_sessions()


def get_all_sessions():
    return session_database.get_all_sessions()


def delete_session(session_id):
    return session_database.delete_session(session_id)
