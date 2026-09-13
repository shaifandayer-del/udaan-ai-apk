import os
import datetime


CONTENT_OUTPUT_FILE = "udaan_content.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def generate_content(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Content AI",
            "message": "Content command is empty."
        }

    prompt = f"""
You are UDAAN AI Content Agent.

Create high-quality original content based on the founder's command.

Founder command:
{command}

Requirements:
- Understand the requested topic.
- Create useful, engaging and original content.
- If it is a video request, create a complete video script.
- If it is a YouTube request, include hook, title, script and CTA.
- If it is a social-media request, create an appropriate post/caption.
- If it is a blog request, create a structured article.
- Use clear language.
- Do not invent real-world facts.
- Do not mention that you are an AI unless requested.
"""

    content = _generate_with_gemini(prompt)

    if not content:
        return {
            "status": "FAILED",
            "agent": "Content AI",
            "message": "Gemini content generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        CONTENT_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
        )
        file.write(
            "UDAAN AI CONTENT\n"
        )
        file.write(
            "================================\n"
        )
        file.write(
            "Time: "
            + timestamp
            + "\n"
        )
        file.write(
            "Command: "
            + command
            + "\n\n"
        )
        file.write(content)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "Content AI",
        "command": command,
        "message": "Content generated successfully.",
        "output_file": CONTENT_OUTPUT_FILE,
        "created_at": timestamp,
        "result": content
    }


def content(command):
    return generate_content(command)


def run(command):
    return generate_content(command)


def execute(command):
    return generate_content(command)


def process(command):
    return generate_content(command)


def handle(command):
    return generate_content(command)


if __name__ == "__main__":
    command = input("Content command: ")
    print(generate_content(command))
