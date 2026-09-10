import importlib


def print_header():
    print()
    print("=" * 60)
    print("                 UDAAN AI")
    print("              COMMAND CENTER")
    print("=" * 60)


def show_menu():
    print()
    print("1. 🧠 AI Command")
    print("2. 🤖 Agents")
    print("3. 📋 Tasks")
    print("4. 📜 History")
    print("5. 📝 Execution Logs")
    print("6. 🚪 Exit")
    print()


def call_function(module_name, function_names, *args):

    try:
        module = importlib.import_module(module_name)

        for function_name in function_names:

            function = getattr(module, function_name, None)

            if callable(function):

                try:
                    return function(*args)
                except TypeError:
                    return function()

        return None

    except Exception as error:
        print("❌", module_name, "error:", error)
        return None


def run_command():

    command = input("🗣️ Command: ").strip()

    if not command:
        print("⚠️ Command empty hai.")
        return

    print()
    print("⚡ Udaan AI processing...")

    try:

        from UdaanCore import process_command

        result = process_command(command)

        print()
        print("📊 RESULT")

        if isinstance(result, dict):

            print("Status :", result.get("status"))
            print("Agent  :", result.get("agent"))
            print("Message:", result.get("message"))

            if result.get("data") is not None:
                print("Data   :", result.get("data"))

            if result.get("error"):
                print("Error  :", result.get("error"))

        else:
            print(result)

    except Exception as error:
        print("❌ Command error:", error)


def show_agents():

    print()
    print("🤖 UDAAN AI AGENTS")
    print("-" * 40)

    result = call_function(
        "AgentManager",
        ["list_agents", "get_agents", "show_agents"]
    )

    if result is None:
        print("Agent list function available nahi hai.")
        print("ℹ️ Agent system separately available hai.")
    else:
        print(result)


def show_tasks():

    print()
    print("📋 UDAAN TASKS")
    print("-" * 40)

    result = call_function(
        "TaskManager",
        ["list_tasks", "get_tasks", "show_tasks", "all_tasks"]
    )

    if result is None:
        print("ℹ️ Task listing function abhi available nahi hai.")
        print("✅ TaskManager module itself accessible hai.")
    else:
        print(result)


def show_history_screen():

    print()
    print("📜 UDAAN HISTORY")
    print("-" * 40)

    result = call_function(
        "UdaanHistory",
        ["show_history", "history", "get_history"]
    )

    if result is None:
        print("ℹ️ History display function available nahi hai.")
    else:
        print(result)


def show_logs_screen():

    print()
    print("📝 EXECUTION LOGS")
    print("-" * 40)

    result = call_function(
        "ExecutionLogs",
        [
            "show_logs",
            "show_execution_logs",
            "display_logs",
            "history"
        ]
    )

    if result is None:
        print("ℹ️ Log display function available nahi hai.")
    else:
        print(result)


def start_ui():

    while True:

        print_header()
        show_menu()

        choice = input("👉 Select: ").strip()

        if choice == "1":
            run_command()

        elif choice == "2":
            show_agents()

        elif choice == "3":
            show_tasks()

        elif choice == "4":
            show_history_screen()

        elif choice == "5":
            show_logs_screen()

        elif choice == "6":
            print()
            print("👋 Udaan AI Command Center closed.")
            break

        else:
            print("⚠️ Invalid option.")

        input("\n↩️ Enter dabao continue karne ke liye...")


if __name__ == "__main__":
    start_ui()