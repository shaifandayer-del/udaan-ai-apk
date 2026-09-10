# ==========================================
# UDAAN AI - MAIN COMMAND ROUTER
# STEP 4
# ==========================================

from AgentConnector import run_agent


def select_agent(command):

    text = command.lower()

    if any(word in text for word in [
        "research", "research karo", "trend", "jaankari", "जानकारी"
    ]):
        return "Research AI"

    if any(word in text for word in [
        "script", "content", "caption", "post", "लेख"
    ]):
        return "Content AI"

    if any(word in text for word in [
        "video", "वीडियो", "reel", "short"
    ]):
        return "Video AI"

    if any(word in text for word in [
        "youtube", "यूट्यूब"
    ]):
        return "YouTube AI"

    if any(word in text for word in [
        "instagram", "social", "इंस्टाग्राम", "सोशल"
    ]):
        return "Social AI"

    if any(word in text for word in [
        "analytics", "analysis", "data", "performance"
    ]):
        return "Analytics AI"

    if any(word in text for word in [
        "marketing", "marketing karo", "advertisement"
    ]):
        return "Marketing AI"

    if any(word in text for word in [
        "app", "software", "code", "coding",
        "developer", "website"
    ]):
        return "Developer AI"

    if any(word in text for word in [
        "automation", "automate", "automatic"
    ]):
        return "Automation AI"

    if any(word in text for word in [
        "creative", "idea", "thumbnail", "creative idea"
    ]):
        return "Creative AI"

    return "Main AI"


def process_command(command):

    if not command.strip():
        print("⚠️ Command empty hai.")
        return

    print()
    print("========================================")
    print("          UDAAN AI COMMAND")
    print("========================================")

    print("👑 Founder:")
    print(command)

    agent = select_agent(command)

    print()
    print("🧠 Main AI:")
    print("Command analyse kar raha hoon...")

    print()
    print("🤖 Selected Agent:")
    print(agent)

    # Main AI ke paas specific agent nahi hai
    if agent == "Main AI":
        print()
        print("ℹ️ Main AI ko command mili.")
        print("⚠️ Is command ke liye abhi specific agent nahi mila.")
        return

    print()
    print("🔗 Connecting to agent...")

    result = run_agent(agent, command)

    print()
    print("========================================")
    print("              RESULT")
    print("========================================")

    if result is not None:
        print(result)
    else:
        print("⚠️ Agent ne koi result return nahi kiya.")


# ==========================================
# COMMAND LOOP
# ==========================================

if __name__ == "__main__":

    print()
    print("╔════════════════════════════════════╗")
    print("║          UDAAN AI                 ║")
    print("║       MAIN COMMAND CENTER         ║")
    print("╚════════════════════════════════════╝")

    print()
    print("Founder, apna command likhiye.")
    print("Exit ke liye: exit")