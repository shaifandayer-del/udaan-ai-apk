import importlib
import inspect


TARGETS = {
    "TaskManager": [
        "create_task",
        "list_tasks"
    ],

    "UdaanMemory": [
        "save_memory",
        "get_memory"
    ],

    "UdaanAPI": [
        "api_status",
        "start_server",
        "handle_command"
    ],

    "UdaanStatus": [
        "health_check",
        "get_status",
        "system_status"
    ],

    "VideoApprovalController": [
        "create_video_preview",
        "approve_video",
        "reject_video",
        "get_video_preview"
    ]
}


def main():

    print()
    print("=" * 65)
    print("UDAAN AI - FUNCTION DIAGNOSTIC")
    print("=" * 65)

    for module_name, functions in TARGETS.items():

        print()
        print("-" * 65)
        print("MODULE:", module_name)
        print("-" * 65)

        try:

            module = importlib.import_module(module_name)

            print("🟢 MODULE IMPORTED")

        except Exception as e:

            print("🔴 MODULE IMPORT FAILED")
            print("ERROR:", e)
            continue

        for function_name in functions:

            if not hasattr(module, function_name):

                print(
                    f"❌ {function_name} : MISSING"
                )

                continue

            function = getattr(
                module,
                function_name
            )

            try:

                signature = inspect.signature(
                    function
                )

                print(
                    f"🟢 {function_name}{signature}"
                )

            except Exception as e:

                print(
                    f"🟡 {function_name} : "
                    f"FOUND, signature unavailable"
                )

                print("   ", e)

    print()
    print("=" * 65)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 65)
    print()
    print("👉 Is output ka screenshot bhejo.")
    print()


if __name__ == "__main__":
    main()