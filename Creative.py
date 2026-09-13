Creative.py

import datetime

CREATIVE_OUTPUT_FILE = "udaan_creative.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def create_creative(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Creative AI",
            "message": "Creative command is empty."
        }

    prompt = f"""
You are UDAAN AI Creative Agent.

Create an original creative concept based on the founder's command.

Founder command:
{command}

Create the most useful creative output for the request.
Depending on the request, provide:
- creative concept
- visual direction
- headline/title
- captions or copy
- scene ideas
- design ideas
- thumbnail/poster ideas
- branding ideas

Keep the output practical, original and ready to use.
Do not invent personal facts or unsupported real-world claims.
"""

    creative = _generate_with_gemini(prompt)

    if not creative:
        return {
            "status": "FAILED",
            "agent": "Creative AI",
            "message": "Creative generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        CREATIVE_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
            "UDAAN AI CREATIVE OUTPUT\n"
            "================================\n"
        )
        file.write("Time: " + timestamp + "\n")
        file.write("Command: " + command + "\n\n")
        file.write(creative)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "Creative AI",
        "command": command,
        "message": "Creative output generated successfully.",
        "output_file": CREATIVE_OUTPUT_FILE,
        "created_at": timestamp,
        "result": creative
    }


def creative(command):
    return create_creative(command)


def run(command):
    return create_creative(command)


def execute(command):
    return create_creative(command)


def process(command):
    return create_creative(command)


def handle(command):
    return create_creative(command)


if __name__ == "__main__":
    command = input("Creative command: ")
    print(create_creative(command))
