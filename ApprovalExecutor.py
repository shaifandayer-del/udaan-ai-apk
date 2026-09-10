from UdaanRouter import select_agent
from AgentConnector import run_agent
from GeminiBrain import ask_gemini

from UdaanDatabase import (
    setup_database,
    get_tasks,
    update_task
)


def find_task(agent, command):

    setup_database()

    tasks = get_tasks()

    for task in tasks:

        task_id = task[0]
        task_agent = task[1]
        task_command = task[2]
        task_status = task[3]

        if (
            task_agent == agent
            and task_command == command
            and task_status == "PENDING"
        ):
            return task_id

    return None


def execute_approved_action(agent, command):

    print()
    print("================================")
    print("⚡ APPROVED ACTION EXECUTION")
    print("================================")
    print()

    print("🤖 Agent:", agent)
    print("👑 Command:", command)
    print()


    # --------------------------------------
    # FIND RELATED TASK
    # --------------------------------------

    task_id = find_task(
        agent,
        command
    )

    if task_id is not None:

        print(
            "📋 Linked Task ID:",
            task_id
        )

    else:

        print(
            "⚠️ Linked pending task nahi mila."
        )

    print()


    # --------------------------------------
    # MAIN AI
    # --------------------------------------

    if agent == "Main AI":

        print("🧠 Main AI executing...")

        try:

            result = ask_gemini(
                command
            )

            print()
            print("🧠 MAIN AI RESULT")
            print("----------------")
            print(result)

            if task_id is not None:

                update_task(
                    task_id,
                    "COMPLETED"
                )

                print()
                print(
                    "✅ Task marked COMPLETED"
                )

            return result

        except Exception as error:

            print()
            print(
                "❌ Main AI execution error:"
            )

            print(error)

            if task_id is not None:

                update_task(
                    task_id,
                    "FAILED"
                )

                print(
                    "❌ Task marked FAILED"
                )

            return None


    # --------------------------------------
    # AGENT EXECUTION
    # --------------------------------------

    print(
        "🚀 Sending command to agent..."
    )

    try:

        result = run_agent(
            agent,
            command
        )

        print()


        # ----------------------------------
        # SUCCESS
        # ----------------------------------

        if result is not None:

            print(
                "✅ APPROVED ACTION COMPLETED"
            )

            print()

            print(result)

            if task_id is not None:

                update_task(
                    task_id,
                    "COMPLETED"
                )

                print()
                print(
                    "✅ Task marked COMPLETED"
                )


        # ----------------------------------
        # FAILURE
        # ----------------------------------

        else:

            print(
                "❌ Agent ne result return nahi kiya."
            )

            if task_id is not None:

                update_task(
                    task_id,
                    "FAILED"
                )

                print(
                    "❌ Task marked FAILED"
                )


        return result


    except Exception as error:

        print()
        print(
            "❌ ACTION EXECUTION ERROR:"
        )

        print(error)


        if task_id is not None:

            update_task(
                task_id,
                "FAILED"
            )

            print(
                "❌ Task marked FAILED"
            )

        return None


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print()
    print("================================")
    print("   UDAAN AI APPROVAL EXECUTOR")
    print("================================")
    print()

    test_command = (
        "YouTube ke liye video publish karo"
    )

    agent = select_agent(
        test_command
    )

    print(
        "Test Agent:",
        agent
    )

    print()

    execute_approved_action(
        agent,
        test_command
    )