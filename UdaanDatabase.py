import json
import os
import sqlite3
import threading
from datetime import datetime, timezone


DATABASE_FILE = os.getenv(
    "UDAAN_DATABASE",
    "udaan.db"
)

_json_lock = threading.Lock()


def _now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def get_connection():
    connection = sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def setup_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                agent TEXT,
                status TEXT,
                result TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE,
                command TEXT,
                agent TEXT,
                status TEXT,
                result TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                agent TEXT,
                status TEXT,
                message TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()

    return True


def initialize_database():
    return setup_database()


def database_ready():
    try:
        setup_database()
        return True
    except Exception:
        return False


def save_command(
    command,
    agent=None,
    status="PENDING",
    result=None
):
    setup_database()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO commands
            (
                command,
                agent,
                status,
                result,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(command or ""),
                agent,
                status,
                json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
                if result is not None
                else None,
                _now()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def update_command(
    command_id,
    status,
    result=None
):
    setup_database()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE commands
            SET status = ?, result = ?
            WHERE id = ?
            """,
            (
                status,
                json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
                if result is not None
                else None,
                command_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def get_command(command_id):
    setup_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT *
            FROM commands
            WHERE id = ?
            """,
            (command_id,)
        ).fetchone()

        if row is None:
            return None

        item = dict(row)

        if item.get("result"):
            try:
                item["result"] = json.loads(
                    item["result"]
                )
            except Exception:
                pass

        return item

    finally:
        connection.close()


def get_commands(limit=100):
    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM commands
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),)
        ).fetchall()

        results = []

        for row in rows:
            item = dict(row)

            if item.get("result"):
                try:
                    item["result"] = json.loads(
                        item["result"]
                    )
                except Exception:
                    pass

            results.append(item)

        return results

    finally:
        connection.close()


def save_task(
    task_id,
    command,
    agent=None,
    status="PENDING",
    result=None
):
    setup_database()

    connection = get_connection()

    timestamp = _now()

    try:
        connection.execute(
            """
            INSERT INTO tasks
            (
                task_id,
                command,
                agent,
                status,
                result,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id)
            DO UPDATE SET
                command = excluded.command,
                agent = excluded.agent,
                status = excluded.status,
                result = excluded.result,
                updated_at = excluded.updated_at
            """,
            (
                str(task_id),
                str(command or ""),
                agent,
                status,
                json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
                if result is not None
                else None,
                timestamp,
                timestamp
            )
        )

        connection.commit()

        return str(task_id)

    finally:
        connection.close()


def update_task(
    task_id,
    status,
    result=None
):
    setup_database()

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE tasks
            SET
                status = ?,
                result = ?,
                updated_at = ?
            WHERE task_id = ?
            """,
            (
                status,
                json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
                if result is not None
                else None,
                _now(),
                str(task_id)
            )
        )

        connection.commit()

        return True

    finally:
        connection.close()


def get_task(task_id):
    setup_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT *
            FROM tasks
            WHERE task_id = ?
            """,
            (str(task_id),)
        ).fetchone()

        if row is None:
            return None

        item = dict(row)

        if item.get("result"):
            try:
                item["result"] = json.loads(
                    item["result"]
                )
            except Exception:
                pass

        return item

    finally:
        connection.close()


def get_tasks(limit=100):
    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM tasks
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),)
        ).fetchall()

        results = []

        for row in rows:
            item = dict(row)

            if item.get("result"):
                try:
                    item["result"] = json.loads(
                        item["result"]
                    )
                except Exception:
                    pass

            results.append(item)

        return results

    finally:
        connection.close()


def save_execution_log(
    command,
    agent=None,
    status="INFO",
    message=""
):
    setup_database()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO execution_logs
            (
                command,
                agent,
                status,
                message,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(command or ""),
                agent,
                status,
                str(message or ""),
                _now()
            )
        )

        connection.commit()

        return True

    finally:
        connection.close()


def get_execution_logs(limit=100):
    setup_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM execution_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),)
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def set_system_state(
    key,
    value
):
    setup_database()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO system_state
            (
                key,
                value,
                updated_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(key)
            DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (
                str(key),
                json.dumps(
                    value,
                    ensure_ascii=False,
                    default=str
                ),
                _now()
            )
        )

        connection.commit()

        return True

    finally:
        connection.close()


def get_system_state(key):
    setup_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT value
            FROM system_state
            WHERE key = ?
            """,
            (str(key),)
        ).fetchone()

        if row is None:
            return None

        try:
            return json.loads(
                row["value"]
            )
        except Exception:
            return row["value"]

    finally:
        connection.close()


def get_database_status():
    try:
        setup_database()

        connection = get_connection()

        try:
            command_count = connection.execute(
                "SELECT COUNT(*) AS count FROM commands"
            ).fetchone()["count"]

            task_count = connection.execute(
                "SELECT COUNT(*) AS count FROM tasks"
            ).fetchone()["count"]

            log_count = connection.execute(
                "SELECT COUNT(*) AS count FROM execution_logs"
            ).fetchone()["count"]

        finally:
            connection.close()

        return {
            "status": "READY",
            "database": DATABASE_FILE,
            "commands": command_count,
            "tasks": task_count,
            "execution_logs": log_count
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "database": DATABASE_FILE,
            "error": str(error)
        }


def close_database():
    return True


setup_database()
