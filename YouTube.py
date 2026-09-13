import datetime
import os

YOUTUBE_OUTPUT_FILE = "udaan_youtube.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def create_youtube_content(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "YouTube AI",
            "message": "YouTube command is empty."
        }

    prompt = f"""
You are UDAAN AI YouTube Agent.

Prepare a complete YouTube content package from the founder's command.

Founder command:
{command}

Provide:
1. Video title
2. Strong opening hook
3. Complete video script
4. Description
5. Relevant keywords
6. Thumbnail concept
7. Call to action

Make the content original, engaging and ready for production.
Do not invent unsupported facts.
"""

    content = _generate_with_gemini(prompt)

    if not content:
        return {
            "status": "FAILED",
            "agent": "YouTube AI",
            "message": "YouTube content generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        YOUTUBE_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
            "UDAAN AI YOUTUBE CONTENT\n"
            "================================\n"
        )
        file.write("Time: " + timestamp + "\n")
        file.write("Command: " + command + "\n\n")
        file.write(content)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "YouTube AI",
        "command": command,
        "message": "YouTube content generated successfully.",
        "output_file": YOUTUBE_OUTPUT_FILE,
        "created_at": timestamp,
        "result": content
    }


def youtube(command):
    return create_youtube_content(command)


def run(command):
    return create_youtube_content(command)


def execute(command):
    return create_youtube_content(command)


def process(command):
    return create_youtube_content(command)


def handle(command):
    return create_youtube_content(command)


if __name__ == "__main__":
    command = input("YouTube command: ")
    print(create_youtube_content(command))
