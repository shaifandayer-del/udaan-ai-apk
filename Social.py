import datetime

SOCIAL_OUTPUT_FILE = "udaan_social.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def create_social_content(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Social AI",
            "message": "Social media command is empty."
        }

    prompt = f"""
You are UDAAN AI Social Media Agent.

Create a complete social-media content package from the founder's command.

Founder command:
{command}

Prepare suitable content for platforms such as:
- Instagram
- Facebook
- X
- LinkedIn

Provide:
1. Main post/caption
2. Strong opening hook
3. Short-form version
4. Relevant hashtags
5. Call to action
6. Visual/content idea

Adapt the tone and length appropriately.
Make everything original and ready to publish.
Do not invent unsupported facts.
"""

    content = _generate_with_gemini(prompt)

    if not content:
        return {
            "status": "FAILED",
            "agent": "Social AI",
            "message": "Social content generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        SOCIAL_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
            "UDAAN AI SOCIAL CONTENT\n"
            "================================\n"
        )
        file.write("Time: " + timestamp + "\n")
        file.write("Command: " + command + "\n\n")
        file.write(content)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "Social AI",
        "command": command,
        "message": "Social content generated successfully.",
        "output_file": SOCIAL_OUTPUT_FILE,
        "created_at": timestamp,
        "result": content
    }


def social(command):
    return create_social_content(command)


def run(command):
    return create_social_content(command)


def execute(command):
    return create_social_content(command)


def process(command):
    return create_social_content(command)


def handle(command):
    return create_social_content(command)


if __name__ == "__main__":
    command = input("Social command: ")
    print(create_social_content(command))
