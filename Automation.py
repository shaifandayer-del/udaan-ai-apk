import datetime
import json

AUTOMATION_OUTPUT_FILE = "udaan_automation.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def create_automation(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Automation AI",
            "message": "Automation command is empty."
        }

    prompt = f"""
You are UDAAN AI Automation Agent.

Design a practical automation workflow from the founder's command.

Founder command:
{command}

Provide:
1. Automation objective
2. Trigger
3. Required inputs
4. Step-by-step workflow
5. Required agents or services
6. Expected output
7. Error handling
8. Approval requirements
9. Next actions

Important:
- Do not claim an automation was executed unless it actually was.
- Do not invent credentials, API results, or completed actions.
- High-impact actions such as publishing, uploading, deleting,
  deploying, or financial actions must require Founder Approval.
- Make the workflow practical and production-ready.
"""

    result = _generate_with_gemini(prompt)

    if not result:
        return {
            "status": "FAILED",
            "agent": "Automation AI",
            "message": "Automation generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        AUTOMATION_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
            "UDAAN AI AUTOMATION WORKFLOW\n"
            "================================\n"
        )
        file.write("Time: " + timestamp + "\n")
        file.write("Command: " + command + "\n\n")
        file.write(result)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "Automation AI",
        "command": command,
        "message": "Automation workflow generated successfully.",
        "output_file": AUTOMATION_OUTPUT_FILE,
        "created_at": timestamp,
        "result": result
    }


def automation(command):
    return create_automation(command)


def run(command):
    return create_automation(command)


def execute(command):
    return create_automation(command)


def process(command):
    return create_automation(command)


def handle(command):
    return create_automation(command)


if __name__ == "__main__":
    command = input("Automation command: ")
    print(json.dumps(
        create_automation(command),
        ensure_ascii=False,
        indent=2
    ))
