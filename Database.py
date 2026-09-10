# ==========================================
# UDAAN AI - DATABASE INTEGRITY TEST
# STEP 75
# ==========================================

import sqlite3

from UdaanDatabase import (
    setup_database
)


DB_NAME = "udaan_ai.db"


TABLES = [
    "tasks",
    "approvals",
    "execution_logs",
    "memories",
]


def check_database():

    print()
    print("================================")
    print("      UDAAN DATABASE TEST")
    print("           STEP 75")
    print("================================")
    print()

    try:

        setup_database()

        print("🗄️ Database initialized")
        print()

    except Exception as error:

        print("🔴 Database initialization failed")
        print(error)
        return

    try:

        connection = sqlite3.connect(
            DB_NAME
        )

        cursor = connection.cursor()

        passed = 0
        failed = 0

        for table in TABLES:

            try:

                cursor.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name=?",
                    (table,)
                )

                result = cursor.fetchone()

                if result:

                    print(
                        "🟢",
                        table,
                        "-> ONLINE"
                    )

                    passed += 1

                else:

                    print(
                        "🔴",
                        table,
                        "-> MISSING"
                    )

                    failed += 1

            except Exception as error:

                print(
                    "🔴",
                    table,
                    "-> ERROR"
                )

                print(
                    "   Reason:",
                    error
                )

                failed += 1

        connection.close()

        print()
        print("--------------------------------")
        print("📊 TABLES:", len(TABLES))
        print("🟢 PASS :", passed)
        print("🔴 FAIL :", failed)
        print("--------------------------------")
        print()

        if failed == 0:

            print(
                "🎉 DATABASE INTEGRITY CHECK PASSED"
            )

        else:

            print(
                "⚠️ DATABASE NEEDS ATTENTION"
            )

        print()

    except Exception as error:

        print("🔴 Database test error:")
        print(error)


if __name__ == "__main__":

    check_database()