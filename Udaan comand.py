# ==========================================
# UDAAN AI - COMMAND CENTER
# STEP 2
# ==========================================

print("================================")
print("        UDAAN AI")
print("     COMMAND CENTER")
print("================================")
print()
print("Available AI:")
print("1. Research AI")
print("2. Content AI")
print("3. Video AI")
print("4. YouTube AI")
print("5. Social AI")
print("6. Analytics AI")
print("7. Marketing AI")
print("8. Developer AI")
print("9. Automation AI")
print("10. Creative AI")
print("0. Exit")
print()


def command_router(command):

    command = command.lower().strip()

    if "research" in command or "research" in command:
        return "Research AI"

    if "script" in command or "content" in command:
        return "Content AI"

    if "video" in command:
        return "Video AI"

    if "youtube" in command:
        return "YouTube AI"

    if "instagram" in command or "social" in command:
        return "Social AI"

    if "analytics" in command or "analysis" in command:
        return "Analytics AI"

    if "marketing" in command:
        return "Marketing AI"

    if (
        "app" in command
        or "software" in command
        or "code" in command
        or "developer" in command
    ):
        return "Developer AI"

    if "automation" in command or "automate" in command:
        return "Automation AI"

    if (
        "idea" in command
        or "creative" in command
        or "thumbnail" in command
    ):
        return "Creative AI"

    return "Main AI"


while True:

    user_command = input("👑 Founder Command: ")

    if user_command.lower().strip() == "0":
        print()
        print("UDAAN AI CLOSED")
        break

    if not user_command.strip():
        print("⚠️ Command empty hai.")
        print()
        continue

    selected_ai = command_router(user_command)

    print()
    print("🧠 Main AI received command:")
    print(user_command)

    print()
    print("🤖 Selected Agent:")
    print(selected_ai)

    print()
    print("--------------------------------")
    print()