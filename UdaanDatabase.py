import sqlite3

DB_NAME = "udaan_ai.db"


def connect():
    return sqlite3.connect(DB_NAME)


def setup_database():

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            command TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            command TEXT NOT NULL,
            result TEXT,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# TASKS
# ==========================================

def add_task(agent, command):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (agent, command, status)
        VALUES (?, ?, ?)
    """, (agent, command, "PENDING"))

    task_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return task_id


def get_tasks():

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, agent, command, status, created_at
        FROM tasks
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def update_task(task_id, status):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ?
    """, (status, task_id))

    connection.commit()
    connection.close()


# ==========================================
# APPROVALS
# ==========================================

def add_approval(agent, action, details):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO approvals
        (agent, action, details, status)
        VALUES (?, ?, ?, ?)
    """, (agent, action, details, "PENDING"))

    approval_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return approval_id


def get_approvals():

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, agent, action, details, status, created_at
        FROM approvals
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def update_approval(approval_id, status):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE approvals
        SET status = ?
        WHERE id = ?
    """, (status, approval_id))

    connection.commit()
    connection.close()


# ==========================================
# EXECUTION LOGS
# ==========================================

def add_execution_log(agent, command, result, status):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO execution_logs
        (agent, command, result, status)
        VALUES (?, ?, ?, ?)
    """, (
        agent,
        command,
        result,
        status
    ))

    log_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return log_id


def get_execution_logs():

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            agent,
            command,
            result,
            status,
            created_at
        FROM execution_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("================================")
    print("     UDAAN AI DATABASE")
    print("================================")
    print()

    setup_database()

    print("✅ Database connected")
    print("✅ Tasks table ready")
    print("✅ Approvals table ready")
    print("✅ Execution Logs table ready")
    print()
    print("🗄️ Database:", DB_NAME)