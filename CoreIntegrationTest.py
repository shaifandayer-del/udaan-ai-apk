from UdaanCore import process_command, get_core_state


def test_command(command):

    print()
    print("-" * 60)
    print("🗣️ COMMAND:", command)

    result = process_command(command)

    print("📊 STATUS :", result.get("status"))
    print("🤖 AGENT  :", result.get("agent"))
    print("💬 MESSAGE:", result.get("message"))
    print("🔵 CORE   :", get_core_state())


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — CORE INTEGRATION TEST")
    print("=" * 60)

    commands = [
        "research latest AI trends",
        "create a video",
        "make an Instagram post",
        "check analytics",
        "build an app",
        "automate my workflow",
        "upload video to YouTube"
    ]

    for command in commands:
        test_command(command)

    print()
    print("=" * 60)
    print("✅ CORE INTEGRATION TEST COMPLETE")
    print("=" * 60)