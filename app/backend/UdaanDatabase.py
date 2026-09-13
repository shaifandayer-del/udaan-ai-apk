import os
import sqlite3
import threading
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "udaan.db")

_db_lock = threading.RLock()


def _now():
    return datetime.utcnow().isoformat()


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    with _db_lock:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    agent TEXT,
                    status TEXT,
                    result TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    agent TEXT,
                    status TEXT,
                    result TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT,
                    status TEXT,
                    details TEXT,
                    created_at TEXT
                )
            """)

            connection.commit()

        finally:
            connection.close()


def initialize_database():
    setup_database()


def save_execution(
    command="",
    agent="",
    status="PENDING",
    result=""
):
    setup_database()

    now = _now()

    with _db_lock:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO executions
                (
                    command,
                    agent,
                    status,
                    result,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    command,
                    agent,
                    status,
                    result,
                    now,
                    now
                )
            )

            execution_id = cursor.lastrowid
            connection.commit()

            return execution_id

        finally:
            connection.close()


def log_execution(
    command="",
    agent="",
    status="PENDING",
    result=""
):
    return save_execution(
        command,
        agent,
        status,
        result
    )


def update_execution(
    execution_id,
    status=None,
    result=None
):
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            if status is not None:
                cursor.execute(
                    """
                    UPDATE executions
                    SET status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        status,
                        _now(),
                        execution_id
                    )
                )

            if result is not None:
                cursor.execute(
                    """
                    UPDATE executions
                    SET result = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        result,
                        _now(),
                        execution_id
                    )
                )

            connection.commit()

            return True

        finally:
            connection.close()


def get_execution(execution_id):
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT *
                FROM executions
                WHERE id = ?
                """,
                (execution_id,)
            ).fetchone()

            return dict(row) if row else None

        finally:
            connection.close()


def get_all_executions():
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM executions
                ORDER BY id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()


def save_task(
    command="",
    agent="",
    status="PENDING",
    result=""
):
    setup_database()

    now = _now()

    with _db_lock:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO tasks
                (
                    command,
                    agent,
                    status,
                    result,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    command,
                    agent,
                    status,
                    result,
                    now,
                    now
                )
            )

            task_id = cursor.lastrowid
            connection.commit()

            return task_id

        finally:
            connection.close()


def update_task(
    task_id,
    status=None,
    result=None
):
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            if status is not None:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        status,
                        _now(),
                        task_id
                    )
                )

            if result is not None:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET result = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        result,
                        _now(),
                        task_id
                    )
                )

            connection.commit()

            return True

        finally:
            connection.close()


def get_task(task_id):
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT *
                FROM tasks
                WHERE id = ?
                """,
                (task_id,)
            ).fetchone()

            return dict(row) if row else None

        finally:
            connection.close()


def get_all_tasks():
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM tasks
                ORDER BY id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()


def save_system_log(
    event="",
    status="INFO",
    details=""
):
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO system_logs
                (
                    event,
                    status,
                    details,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    event,
                    status,
                    details,
                    _now()
                )
            )

            connection.commit()

        finally:
            connection.close()


def get_system_logs(limit=100):
    setup_database()

    with _db_lock:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM system_logs
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()


def get_database_status():
    setup_database()

    return {
        "status": "READY",
        "database": DATABASE_PATH,
        "database_exists": os.path.exists(
            DATABASE_PATH
        )
    }


setup_database()
