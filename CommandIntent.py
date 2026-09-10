from UdaanRouter import select_agent


PROTECTED_WORDS = [
    "publish",
    "upload",
    "deploy",
    "delete",
    "post",
    "send",
    "release",
    "live",
    "shutdown",
    "remove"
]


def detect_action(command):

    text = command.lower()

    if any(word in text for word in ["research", "research karo", "trend"]):
        return "RESEARCH"

    if any(word in text for word in ["script", "content", "caption"]):
        return "CONTENT"

    if any(word in text for word in ["video", "reel", "short"]):
        return "VIDEO"

    if any(word in text for word in ["youtube", "यूट्यूब"]):
        return "YOUTUBE"

    if any(word in text for word in ["instagram", "social", "इंस्टाग्राम"]):
        return "SOCIAL"

    if any(word in text for word in ["analytics", "analysis", "performance"]):
        return "ANALYTICS"

    if "marketing" in text:
        return "MARKETING"

    if any(word in text for word in ["app", "software", "coding", "code", "developer"]):
        return "DEVELOPER"

    if any(word in text for word in ["automation", "automate", "automatic"]):
        return "AUTOMATION"

    if any(word in text for word in ["creative", "idea", "thumbnail"]):
        return "CREATIVE"

    return "GENERAL"


def detect_priority(command):

    text = command.lower()

    if any(word in text for word in ["urgent", "jaldi", "immediately", "abhi"]):
        return "HIGH"

    if any(word in text for word in ["important", "priority"]):
        return "HIGH"

    return "NORMAL"


def requires_approval(command):

    text = command.lower()

    for word in PROTECTED_WORDS:
        if word in text:
            return True

    return False


def analyze_command(command):

    agent = select_agent(command)

    return {
        "command": command,
        "agent": agent,
        "action": detect_action(command),
        "priority": detect_priority(command),
        "approval_required": requires_approval(command)
    }


def show_intent(command):

    result = analyze_command(command)

    print()
    print("================================")
    print("       UDAAN COMMAND INTENT")
    print("================================")
    print()

    print("📝 Command :", result["command"])
    print("🤖 Agent   :", result["agent"])
    print("⚡ Action  :", result["action"])
    print("🔥 Priority:", result["priority"])

    if result["approval_required"]:
        print("🔐 Approval: REQUIRED")
    else:
        print("🟢 Approval: NOT REQUIRED")

    print()
    print("================================")
    print()


if __name__ == "__main__":

    command = input("👑 Command: ")

    show_intent(command)