import sqlite3

DB_NAME = "udaan_ai.db"


def show_approval_queue():

    print()
    print("=" * 60)
    print("             UDAAN AI")
    print("          FOUNDER APPROVAL QUEUE")
    print("=" * 60)

    try:

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='approvals'"
        )

        if cursor.fetchone() is None:
            print()
            print("⚠️ Approvals table nahi mili.")
            connection.close()
            return

        cursor.execute("PRAGMA table_info(approvals)")
        columns = cursor.fetchall()

        if not columns:
            print()
            print("⚠️ Approvals table empty/invalid hai.")
            connection.close()
            return

        column_names = [column[1] for column in columns]

        print()
        print("📋 Approval Table Fields:")
        print("-" * 40)

        for column in column_names:
            print("•", column)

        cursor.execute("SELECT * FROM approvals")

        rows = cursor.fetchall()

        print()
        print("📊 APPROVAL RECORDS")
        print("-" * 40)

        if not rows:

            print("✅ No pending approval records.")

        else:

            for index, row in enumerate(rows, 1):

                print()
                print("Approval #", index)

                for name, value in zip(column_names, row):
                    print(f"{name}: {value}")

        connection.close()

    except Exception as error:

        print()
        print("❌ Approval queue error:")
        print(error)

    print()
    print("=" * 60)


if __name__ == "__main__":
    show_approval_queue()