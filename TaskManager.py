from UdaanDatabase import (
    setup_database,
    add_task,
    get_tasks,
    update_task
)


def create_task(agent, command):

    setup_database()

    task_id = add_task(
        agent,
        command
    )

    print()
    print("📋 TASK CREATED")
    print("----------------")
    print("🆔 Task ID:", task_id)
    print("🤖 Agent:", agent)
    print("📋 Command:", command)
    print("⏳ Status: PENDING")
    print()

    return {
        "id": task_id,
        "agent": agent,
        "command": command,
        "status": "PENDING"
    }


def show_tasks():

    setup_database()

    tasks = get_tasks()

    print()
    print("================================")
    print("          📋 UDAAN TASKS")
    print("================================")
    print()

    if not tasks:
        print("📭 Koi task nahi hai.")
        print()
        return

    for task in tasks:

        print("🆔 ID:", task[0])
        print("🤖 Agent:", task[1])
        print("📋 Command:", task[2])
        print("📌 Status:", task[3])
        print("🕒 Created:", task[4])

        print("------------------------------")

    print()


def complete_task(task_id):

    setup_database()

    tasks = get_tasks()

    found = False

    for task in tasks:

        if task[0] == task_id:

            found = True

            if task[3] == "COMPLETED":
                print("⚠️ Task already completed.")
                return

            update_task(
                task_id,
                "COMPLETED"
            )

            print()
            print("✅ TASK COMPLETED")
            print("🆔 Task ID:", task_id)
            print()

            return

    if not found:

        print(
            "❌ Task ID nahi mila:",
            task_id
        )


def fail_task(task_id):

    setup_database()

    tasks = get_tasks()

    found = False

    for task in tasks:

        if task[0] == task_id:

            found = True

            update_task(
                task_id,
                "FAILED"
            )

            print()
            print("❌ TASK FAILED")
            print("🆔 Task ID:", task_id)
            print()

            return

    if not found:

        print(
            "❌ Task ID nahi mila:",
            task_id
        )


def cancel_task(task_id):

    setup_database()

    tasks = get_tasks()

    found = False

    for task in tasks:

        if task[0] == task_id:

            found = True

            update_task(
                task_id,
                "CANCELLED"
            )

            print()
            print("🚫 TASK CANCELLED")
            print("🆔 Task ID:", task_id)
            print()

            return

    if not found:

        print(
            "❌ Task ID nahi mila:",
            task_id
        )


if __name__ == "__main__":

    setup_database()

    create_task(
        "Research AI",
        "India ke latest AI trends research karo"
    )

    create_task(
        "Content AI",
        "AI par YouTube script banao"
    )

    show_tasks()