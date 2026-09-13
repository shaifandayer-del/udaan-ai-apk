import datetime
import os

DEVELOPER_OUTPUT_FILE = "udaan_developer.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def create_developer_output(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Developer AI",
            "message": "Developer command is empty."
        }

    prompt = f"""
You are UDAAN AI Developer Agent.

Help the founder build, debug, improve, or design software.

Founder command:
{command}

Requirements:
- Understand the requested software task.
- Provide a practical technical solution.
- If code is requested, provide complete usable code.
- Identify required files and dependencies.
- Explain important implementation decisions briefly.
- For debugging, identify the likely cause and give the exact fix.
- Never claim that code was executed or tested unless execution actually happened.
- Never invent files, APIs, credentials, test results, or system capabilities.
- Prefer safe, maintainable and production-ready solutions.
"""

    result = _generate_with_gemini(prompt)

    if not result:
        return {
            "status": "FAILED",
            "agent": "Developer AI",
            "message": "Developer AI generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        DEVELOPER_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
            "UDAAN AI DEVELOPER OUTPUT\n"
            "================================\n"
        )
        file.write("Time: " + timestamp + "\n")
        file.write("Command: " + command + "\n\n")
        file.write(result)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "Developer AI",
        "command": command,
        "message": "Developer output generated successfully.",
        "output_file": DEVELOPER_OUTPUT_FILE,
        "created_at": timestamp,
        "result": result
    }


def developer(command):
    return create_developer_output(command)


def run(command):
    return create_developer_output(command)


def execute(command):
    return create_developer_output(command)


def process(command):
    return create_developer_output(command)


def handle(command):
    return create_developer_output(command)


if __name__ == "__main__":
    command = input("Developer command: ")
    print(create_developer_output(command))
