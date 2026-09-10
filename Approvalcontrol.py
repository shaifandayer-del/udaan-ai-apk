import sqlite3

DB_NAME = "udaan_ai.db"

STATUS_COLUMNS = [
    "status",
    "approval_status",
    "state"
]


def get_approval_columns(cursor):
    cursor.execute("PRAGMA table_info(approvals)")
    columns = cursor.fetchall()
    return [column[1] for column in columns]


def find_status_column(columns):
    for column in STATUS_COLUMNS:
        if column in columns:
            return column
    return None


def show_approvals():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='approvals'"
    )

    if cursor.fetchone() is None:
        connection.close()
        print("❌ approvals table nahi mili.")
        return []

    columns = get_approval_columns(cursor)

    cursor.execute("SELECT rowid, * FROM approvals")
    rows = cursor.fetchall()

    print()
    print("📋 FOUNDER APPROVALS")
    print("-" * 50)

    if not rows:
        print("✅ Approval queue empty.")
        connection.close()
        return []

    for row in rows:
        print()
        print("🆔 Approval Row:", row[0])

        for name, value in zip(columns, row[1:]):
            print(f"{name}: {value}")

    connection.close()

    return rows


def update_approval(row_id, new_status):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='approvals'"
    )

    if cursor.fetchone() is None:
        connection.close()
        print("❌ approvals table nahi mili.")
        return False

    columns = get_approval_columns(cursor)
    status_column = find_status_column(columns)

    if status_column is None:
        connection.close()
        print("❌ Approval status column nahi mila.")
        print("Available columns:", columns)
        return False

    cursor.execute(
        f'UPDATE approvals SET "{status_column}" = ? '
        "WHERE rowid = ?",
        (new_status, row_id)
    )

    changed = cursor.rowcount

    connection.commit()
    connection.close()

    if changed == 0:
        print("❌ Approval ID nahi mila.")
        return False

    print()
    print("✅ Approval updated.")
    print("🆔 Row:", row_id)
    print("📊 Status:", new_status)

    return True


def approval_control():

    print()
    print("=" * 60)
    print("          UDAAN AI — FOUNDER CONTROL")
    print("=" * 60)

    show_approvals()

    print()
    print("1. ✅ Approve")
    print("2. ❌ Reject")
    print("3. 🚪 Exit")

    choice = input("\n👉 Select: ").strip()

    if choice == "3":
        print("👋 Closed.")
        return

    if choice not in ["1", "2"]:
        print("⚠️ Invalid option.")
        return

    row_id = input("🆔 Approval Row ID: ").strip()

    try:
        row_id = int(row_id)
    except ValueError:
        print("❌ Row ID number hona chahiye.")
        return

    if choice == "1":
        update_approval(row_id, "APPROVED")

    elif choice == "2":
        update_approval(row_id, "REJECTED")


if __name__ == "__main__":
    approval_control()