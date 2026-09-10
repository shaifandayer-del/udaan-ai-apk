import sqlite3

DB_NAME = "udaan_ai.db"


def connect():
    return sqlite3.connect(DB_NAME)


def setup_session_database():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            command TEXT NOT NULL,
            agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_session(session_id, started_at):
    setup_session_database()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO sessions
        (session_id, started_at, status)
        VALUES (?, ?, ?)
    """, (session_id, started_at, "ACTIVE"))

    conn.commit()
    conn.close()

    print("💾 Session saved to database")


def save_session_command(session_id, command, agent=""):
    setup_session_database()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO session_commands
        (session_id, command, agent)
        VALUES (?, ?, ?)
    """, (session_id, command, agent))

    conn.commit()
    conn.close()


def close_session(session_id, ended_at):
    setup_session_database()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE sessions
        SET ended_at = ?, status = ?
        WHERE session_id = ?
    """, (ended_at, "CLOSED", session_id))

    conn.commit()
    conn.close()


def get_sessions():
    setup_session_database()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, session_id, started_at, ended_at, status
        FROM sessions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_session_commands(session_id):
    setup_session_database()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, command, agent, created_at
        FROM session_commands
        WHERE session_id = ?
        ORDER BY id DESC
    """, (session_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def show_sessions():
    print()
    print("================================")
    print("     UDAAN AI SESSION DATABASE")
    print("================================")
    print()

    sessions = get_sessions()

    if not sessions:
        print("📭 Koi saved session nahi hai.")
        return

    for session in sessions:
        session_id = session[1]
        started = session[2]
        ended = session[3]
        status = session[4]

        print("🆔 Session:", session_id)
        print("⏰ Started:", started)
        print("🏁 Ended:", ended or "Still active")
        print("📌 Status:", status)
        print("--------------------------------")


if __name__ == "__main__":
    setup_session_database()

    create_session(
        "TEST_SESSION_001",
        "2026-09-07 12:00:00"
    )

    save_session_command(
        "TEST_SESSION_001",
        "YouTube ke liye video idea do",
        "YouTube AI"
    )

    show_sessions()

    print()
    print("✅ SESSION DATABASE WORKING")