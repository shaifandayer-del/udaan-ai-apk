from UdaanDatabase import (
    setup_database,
    get_execution_logs
)


def show_history():

    setup_database()

    logs = get_execution_logs()

    print()
    print("================================")
    print("       🕘 UDAAN AI HISTORY")
    print("================================")
    print()

    if not logs:

        print("📭 Abhi koi activity history nahi hai.")
        print()

        return

    for log in logs:

        log_id = log[0]
        agent = log[1]
        command = log[2]
        result = log[3]
        status = log[4]
        created_at = log[5]

        if status == "SUCCESS":
            status_icon = "✅"
        elif status == "FAILED":
            status_icon = "❌"
        else:
            status_icon = "⏳"

        print("🆔 ID:", log_id)
        print("🤖 Agent:", agent)
        print("👑 Command:", command)
        print(status_icon, "Status:", status)
        print("🕒 Time:", created_at)

        if result:
            print("📄 Result:", result)

        print("------------------------------")

    print()


if __name__ == "__main__":

    show_history()