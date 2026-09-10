# ==========================================
# UDAAN AI - AGENT RESULT STANDARD
# STEP 71
# ==========================================

import datetime


def success_result(
    agent,
    command,
    message="Agent executed successfully.",
    data=None
):

    return {
        "status": "SUCCESS",
        "agent": agent,
        "command": command,
        "message": message,
        "data": data,
        "created_at": datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


def failed_result(
    agent,
    command,
    message,
    error=None
):

    return {
        "status": "FAILED",
        "agent": agent,
        "command": command,
        "message": message,
        "error": error,
        "created_at": datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


def pending_result(
    agent,
    command,
    message="Founder approval required."
):

    return {
        "status": "PENDING_APPROVAL",
        "agent": agent,
        "command": command,
        "message": message,
        "created_at": datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


def show_result(result):

    print()
    print("================================")
    print("       UDAAN AI RESULT")
    print("================================")
    print()

    if not isinstance(result, dict):

        print(result)
        return

    print("📊 Status :", result.get("status"))
    print("🤖 Agent  :", result.get("agent"))
    print("📝 Command:", result.get("command"))
    print("💬 Message:", result.get("message"))

    if result.get("data") is not None:
        print("📦 Data   :", result.get("data"))

    if result.get("error"):
        print("❌ Error  :", result.get("error"))

    print("🕒 Time   :", result.get("created_at"))
    print()


if __name__ == "__main__":

    test = success_result(
        "Test AI",
        "System test",
        "Result system working."
    )

    show_result(test)