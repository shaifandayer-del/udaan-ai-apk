from UdaanCore import process_command


PROTECTED_WORDS = [
    "upload",
    "publish",
    "post",
    "deploy",
    "delete",
    "send"
]


def requires_founder_approval(command):

    if not command:
        return False

    text = command.lower()

    return any(
        word in text
        for word in PROTECTED_WORDS
    )


def submit_command(command):

    if not command or not command.strip():

        return {
            "status": "FAILED",
            "message": "Command empty hai."
        }

    command = command.strip()

    if requires_founder_approval(command):

        return {
            "status": "WAITING_APPROVAL",
            "command": command,
            "message": "Founder approval required.",
            "next_action": "approve_or_reject"
        }

    return process_command(command)


def approval_status(command):

    return {
        "command": command,
        "requires_approval":
            requires_founder_approval(command)
    }


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — FOUNDER APPROVAL API")
    print("=" * 60)

    tests = [
        "research latest AI trends",
        "create a video",
        "upload video to YouTube",
        "publish Instagram post"
    ]

    for command in tests:

        print()
        print("🗣️", command)

        result = submit_command(command)

        print("📊 Status :", result.get("status"))
        print("💬 Message:", result.get("message"))

    print()
    print("=" * 60)
    print("✅ FOUNDER APPROVAL API READY")
    print("=" * 60)