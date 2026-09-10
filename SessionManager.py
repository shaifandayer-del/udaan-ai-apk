import datetime


SESSION = {
    "session_id": None,
    "started_at": None,
    "commands": [],
    "agents_used": [],
    "tasks_created": [],
    "approvals_requested": []
}


def start_session():

    now = datetime.datetime.now()

    SESSION["session_id"] = now.strftime(
        "%Y%m%d%H%M%S"
    )

    SESSION["started_at"] = str(now)

    SESSION["commands"] = []
    SESSION["agents_used"] = []
    SESSION["tasks_created"] = []
    SESSION["approvals_requested"] = []

    print()
    print("🟢 UDAAN AI SESSION STARTED")
    print("🆔 Session ID:", SESSION["session_id"])
    print("⏰ Started:", SESSION["started_at"])
    print()


def add_command(command):

    SESSION["commands"].append({
        "command": command,
        "time": str(datetime.datetime.now())
    })


def add_agent(agent):

    if agent not in SESSION["agents_used"]:
        SESSION["agents_used"].append(agent)


def add_task(task_id):

    SESSION["tasks_created"].append(task_id)


def add_approval(approval_id):

    SESSION["approvals_requested"].append(
        approval_id
    )


def get_session():

    return SESSION


def show_session():

    print()
    print("================================")
    print("       UDAAN AI SESSION")
    print("================================")
    print()

    print(
        "🆔 Session ID:",
        SESSION["session_id"]
    )

    print(
        "⏰ Started:",
        SESSION["started_at"]
    )

    print()

    print(
        "📝 Commands:",
        len(SESSION["commands"])
    )

    print(
        "🤖 Agents Used:",
        len(SESSION["agents_used"])
    )

    print(
        "📋 Tasks Created:",
        len(SESSION["tasks_created"])
    )

    print(
        "🔐 Approvals:",
        len(SESSION["approvals_requested"])
    )

    print()

    if SESSION["agents_used"]:

        print("🤖 Agents:")

        for agent in SESSION["agents_used"]:
            print("   •", agent)

    print()
    print("================================")
    print()


if __name__ == "__main__":

    start_session()

    add_command(
        "YouTube ke liye video idea do"
    )

    add_agent(
        "YouTube AI"
    )

    add_task(1)

    show_session()