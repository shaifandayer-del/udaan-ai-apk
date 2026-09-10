from UdaanCore import process_command


def run_approval_test():

    print()
    print("=" * 60)
    print("          UDAAN AI — APPROVAL SYSTEM TEST")
    print("=" * 60)

    commands = [
        "research latest AI trends",
        "create a YouTube video",
        "upload video to YouTube",
        "publish this content on Instagram"
    ]

    for command in commands:

        print()
        print("🗣️ Command:", command)
        print("-" * 50)

        try:

            result = process_command(command)

            if isinstance(result, dict):

                print("📊 Status :", result.get("status"))
                print("🤖 Agent  :", result.get("agent"))
                print("💬 Message:", result.get("message"))

                if result.get("data") is not None:
                    print("📦 Data   :", result.get("data"))

            else:
                print("Result:", result)

        except Exception as error:

            print("❌ Test error:", error)

    print()
    print("=" * 60)
    print("✅ APPROVAL SYSTEM TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_approval_test()