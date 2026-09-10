import importlib


def show_banner():
    print()
    print("=" * 60)
    print("                 UDAAN AI")
    print("             UNIFIED LAUNCHER")
    print("=" * 60)


def run_module(module_name, function_name=None):

    try:
        module = importlib.import_module(module_name)

        if function_name:
            function = getattr(module, function_name, None)

            if callable(function):
                return function()

        main_function = getattr(module, "main", None)

        if callable(main_function):
            return main_function()

        print("⚠️ Launch function nahi mila:", module_name)

    except Exception as error:
        print("❌ Launch error:", error)


def launch():

    while True:

        show_banner()

        print()
        print("1. 🧠 Command Center")
        print("2. 🩺 System Status")
        print("3. 🧪 Agent Tests")
        print("4. 🔍 System Diagnostic")
        print("5. 🌐 API Server")
        print("6. 🚪 Exit")
        print()

        choice = input("👉 Select: ").strip()

        if choice == "1":

            run_module(
                "UdaanUI",
                "start_ui"
            )

        elif choice == "2":

            run_module(
                "UdaanStatus",
                "show_status"
            )

        elif choice == "3":

            run_module(
                "AgentTest"
            )

        elif choice == "4":

            run_module(
                "SystemDiagnostic"
            )

        elif choice == "5":

            print()
            print("🌐 Starting Udaan API...")
            print("⚠️ API development mode mein hai.")

            run_module(
                "UdaanAPI"
            )

        elif choice == "6":

            print()
            print("👋 Udaan AI Launcher closed.")
            break

        else:

            print()
            print("⚠️ Invalid option.")

        input("\n↩️ Enter dabao continue karne ke liye...")


if __name__ == "__main__":
    launch()