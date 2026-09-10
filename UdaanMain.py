from UdaanDatabase import setup_database
from UdaanMemory import show_memories
from TaskManager import show_tasks
from FounderApproval import show_pending
from ExecutionLogs import show_logs
from UdaanHistory import show_history
from AgentManager import show_agent_manager
from AgentHealth import show_health

from UdaanCore import process_command


def show_status():

    print()
    print("================================")
    print("          UDAAN AI STATUS")
    print("================================")
    print()

    print("🧠 Main AI           : ONLINE")
    print("🎯 Udaan Core        : ONLINE")
    print("🤖 Agent Manager     : ONLINE")
    print("🔐 Founder Approval  : ONLINE")
    print("🗄️ Database          : ONLINE")
    print("📋 Task Manager      : ONLINE")
    print("📊 Execution Logs    : ONLINE")
    print("🧠 Memory            : ONLINE")
    print("❤️ Agent Health      : ONLINE")
    print()


def handle_command(command):

    command = command.strip()

    if not command:
        return

    lower = command.lower()

    # ==========================================
    # SYSTEM COMMANDS
    # ==========================================

    if lower == "status":
        show_status()
        return

    if lower == "health":
        show_health()
        return

    if lower == "agents":
        show_agent_manager()
        return

    if lower == "memory":
        show_memories()
        return

    if lower == "tasks":
        show_tasks()
        return

    if lower == "approvals":
        show_pending()
        return

    if lower == "logs":
        show_logs()
        return

    if lower == "history":
        show_history()
        return

    # ==========================================
    # AI COMMAND
    # ==========================================

    print()
    print("🚀 Processing command...")
    print()

    result = process_command(command)

    print()
    print("================================")
    print("          UDAAN RESULT")
    print("================================")
    print()

    print(result)
    print()


def main():

    setup_database()

    print()
    print("================================")
    print("          UDAAN AI")
    print("       MAIN COMMAND CENTER")
    print("================================")
    print()

    print("Commands:")
    print("status")
    print("health")
    print("agents")
    print("memory")
    print("tasks")
    print("approvals")
    print("logs")
    print("history")
    print("exit")
    print()

    while True:

        try:

            command = input("👑 Udaan AI > ").strip()

            if command.lower() in [
                "exit",
                "quit",
                "0"
            ]:
                print()
                print("👋 Udaan AI shutting down...")
                break

            handle_command(command)

        except KeyboardInterrupt:

            print()
            print("👋 Udaan AI stopped.")
            break

        except Exception as error:

            print()
            print("❌ System Error:")
            print(error)
            print()


if __name__ == "__main__":
    main()