import sqlite3
import os
import datetime


DATABASE_FILE = "udaan.db"


class UdaanDatabase:
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
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    agent TEXT,
                    status TEXT,
                    result TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            connection.execute("""
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
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_key TEXT UNIQUE NOT NULL,
                    memory_value TEXT,
                    updated_at TEXT NOT NULL
                )
            """)

            connection.commit()

        finally:
            connection.close()

    def save_command(
        self,
        command,
        agent=None,
        status="UNKNOWN",
        result=None
    ):
        now = datetime.datetime.now().isoformat()

        connection = self._connect()

        try:
            connection.execute(
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
                    command,
                    agent,
                    status,
                    str(result)
                    if result is not None
                    else None,
                    now
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get_commands(self, limit=50):
        connection = self._connect()

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

            return [
                dict(row)
                for row in rows
            ]

        finally:
            connection.close()

    def save_task(
        self,
        task_id,
        command,
        agent=None,
        status="PENDING",
        result=None
    ):
        now = datetime.datetime.now().isoformat()

        connection = self._connect()

        try:
            connection.execute(
                """
                INSERT OR REPLACE INTO tasks
                (
                    task_id,
                    command,
                    agent,
                    status,
                    result,
                    created_at,
                    updated_at
                )
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    COALESCE(
                        (
                            SELECT created_at
                            FROM tasks
                            WHERE task_id = ?
                        ),
                        ?
                    ),
                    ?
                )
                """,
                (
                    task_id,
                    command,
                    agent,
                    status,
                    str(result)
                    if result is not None
                    else None,
                    task_id,
                    now,
                    now
                )
            )

            connection.commit()

        finally:
            connection.close()

    def update_task(
        self,
        task_id,
        status=None,
        result=None
    ):
        now = datetime.datetime.now().isoformat()

        connection = self._connect()

        try:
            if status is not None:
                connection.execute(
                    """
                    UPDATE tasks
                    SET status = ?,
                        updated_at = ?
                    WHERE task_id = ?
                    """,
                    (
                        status,
                        now,
                        task_id
                    )
                )

            if result is not None:
                connection.execute(
                    """
                    UPDATE tasks
                    SET result = ?,
                        updated_at = ?
                    WHERE task_id = ?
                    """,
                    (
                        str(result),
                        now,
                        task_id
                    )
                )

            connection.commit()

        finally:
            connection.close()

    def get_task(self, task_id):
        connection = self._connect()

        try:
            row = connection.execute(
                """
                SELECT *
                FROM tasks
                WHERE task_id = ?
                """,
                (task_id,)
            ).fetchone()

            return dict(row) if row else None

        finally:
            connection.close()

    def get_tasks(self, limit=50):
        connection = self._connect()

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

            return [
                dict(row)
                for row in rows
            ]

        finally:
            connection.close()

    def remember(self, key, value):
        now = datetime.datetime.now().isoformat()

        connection = self._connect()

        try:
            connection.execute(
                """
                INSERT OR REPLACE INTO memory
                (
                    memory_key,
                    memory_value,
                    updated_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    key,
                    str(value),
                    now
                )
            )

            connection.commit()

        finally:
            connection.close()

    def recall(self, key):
        connection = self._connect()

        try:
            row = connection.execute(
                """
                SELECT memory_value
                FROM memory
                WHERE memory_key = ?
                """,
                (key,)
            ).fetchone()

            return (
                row["memory_value"]
                if row
                else None
            )

        finally:
            connection.close()

    def get_memory(self):
        connection = self._connect()

        try:
            rows = connection.execute(
                """
                SELECT memory_key, memory_value
                FROM memory
                ORDER BY id DESC
                """
            ).fetchall()

            return {
                row["memory_key"]:
                    row["memory_value"]
                for row in rows
            }

        finally:
            connection.close()


database = UdaanDatabase()


def save_command(
    command,
    agent=None,
    status="UNKNOWN",
    result=None
):
    return database.save_command(
        command,
        agent,
        status,
        result
    )


def get_commands(limit=50):
    return database.get_commands(limit)


def save_task(
    task_id,
    command,
    agent=None,
    status="PENDING",
    result=None
):
    return database.save_task(
        task_id,
        command,
        agent,
        status,
        result
    )


def update_task(
    task_id,
    status=None,
    result=None
):
    return database.update_task(
        task_id,
        status,
        result
    )


def get_task(task_id):
    return database.get_task(task_id)


def get_tasks(limit=50):
    return database.get_tasks(limit)


def remember(key, value):
    return database.remember(
        key,
        value
    )


def recall(key):
    return database.recall(key)


def get_memory():
    return database.get_memory()
