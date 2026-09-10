# ==========================================
# UDAAN AI EXECUTION LOGS
# ==========================================

from UdaanDatabase import (
    setup_database,
    get_execution_logs
)


def show_logs(limit=50):

    print()
    print("================================")
    print("       UDAAN AI EXECUTION LOGS")
    print("================================")
    print()

    try:
        setup_database()
    except Exception:
        pass

    try:
        logs = get_execution_logs()

    except TypeError:
        try:
            logs = get_execution_logs(limit)

        except Exception as error:
            print("❌ Logs load failed:")
            print(error)
            return

    except Exception as error:
        print("❌ Logs load failed:")
        print(error)
        return

    if not logs:
        print("📭 No execution logs found.")
        print()
        return

    print("📊 Total Logs:", len(logs))
    print()

    for number, log in enumerate(logs[:limit], 1):

        print("--------------------------------")

        if isinstance(log, dict):

            print("🔢 Log:", number)
            print("Agent:", log.get("agent", "Unknown"))
            print("Command:", log.get("command", "Unknown"))
            print("Status:", log.get("status", "Unknown"))
            print("Time:", log.get(
                "created_at",
                log.get("timestamp", "Unknown")
            ))

            if log.get("error"):
                print("Error:", log.get("error"))

        else:

            print("🔢 Log:", number)
            print(log)

    print("--------------------------------")
    print()


# Compatibility aliases
# Different parts of Udaan AI can use any of these names.

def show_execution_logs():
    return show_logs()


def display_logs():
    return show_logs()


def history():
    return show_logs()


if __name__ == "__main__":

    show_logs()