import sqlite3
import time


DB_NAME = "udaan.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def setup_approval_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approval_requests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            approval_id TEXT UNIQUE,

            action TEXT,

            platform TEXT,

            file_path TEXT,

            title TEXT,

            description TEXT,

            command TEXT,

            agent TEXT,

            status TEXT,

            created_at REAL

        )
    """)

    connection.commit()

    # Existing database ko safely upgrade karne ke liye
    columns = [
        ("command", "TEXT"),
        ("agent", "TEXT")
    ]

    for column_name, column_type in columns:

        try:
            cursor.execute(
                f"ALTER TABLE approval_requests ADD COLUMN {column_name} {column_type}"
            )
        except sqlite3.OperationalError:
            pass

    connection.commit()
    connection.close()


def save_approval(approval):

    setup_approval_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO approval_requests
        (
            approval_id,
            action,
            platform,
            file_path,
            title,
            description,
            command,
            agent,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        approval.get("approval_id"),
        approval.get("action"),
        approval.get("platform"),
        approval.get("file_path"),
        approval.get("title"),
        approval.get("description"),
        approval.get("command"),
        approval.get("agent"),
        approval.get("status"),
        time.time()

    ))

    connection.commit()
    connection.close()

    return True


def update_approval_status(
    approval_id,
    status
):

    setup_approval_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE approval_requests
        SET status = ?
        WHERE approval_id = ?
    """, (
        status,
        approval_id
    ))

    connection.commit()

    changed = cursor.rowcount

    connection.close()

    return changed > 0


def get_approval_from_db(
    approval_id
):

    setup_approval_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            approval_id,
            action,
            platform,
            file_path,
            title,
            description,
            command,
            agent,
            status,
            created_at
        FROM approval_requests
        WHERE approval_id = ?
    """, (
        approval_id,
    ))

    row = cursor.fetchone()

    connection.close()

    if not row:
        return None

    return {
        "approval_id": row[0],
        "action": row[1],
        "platform": row[2],
        "file_path": row[3],
        "title": row[4],
        "description": row[5],
        "command": row[6],
        "agent": row[7],
        "status": row[8],
        "created_at": row[9]
    }


def get_pending_approvals_db():

    setup_approval_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            approval_id,
            action,
            platform,
            file_path,
            title,
            description,
            command,
            agent,
            status,
            created_at
        FROM approval_requests
        WHERE status = 'PENDING'
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    approvals = []

    for row in rows:

        approvals.append({
            "approval_id": row[0],
            "action": row[1],
            "platform": row[2],
            "file_path": row[3],
            "title": row[4],
            "description": row[5],
            "command": row[6],
            "agent": row[7],
            "status": row[8],
            "created_at": row[9]
        })

    return approvals


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — APPROVAL DATABASE TEST")
    print("=" * 60)

    setup_approval_table()

    test_approval = {
        "approval_id": "TEST-001",
        "action": "UPLOAD_VIDEO",
        "platform": "YouTube",
        "file_path": "udaan_videos/test.mp4",
        "title": "Udaan Test Video",
        "description": "Approval database test",
        "command": "Upload test video to YouTube",
        "agent": "YouTube AI",
        "status": "PENDING"
    }

    save_approval(test_approval)

    print()
    print("💾 Approval saved.")

    print()
    print("📋 Pending approvals:")

    print(
        get_pending_approvals_db()
    )

    print()
    print("🔎 Single approval:")

    print(
        get_approval_from_db("TEST-001")
    )

    print()
    print("=" * 60)
    print("✅ APPROVAL DATABASE READY")
    print("=" * 60)
