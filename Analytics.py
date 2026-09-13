import datetime
import json

ANALYTICS_OUTPUT_FILE = "udaan_analytics.txt"


def _generate_with_gemini(prompt):
    try:
        from GeminiBrain import ask_gemini

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as error:
        print("GeminiBrain error:", error)

    return ""


def analyze(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Analytics AI",
            "message": "Analytics command is empty."
        }

    prompt = f"""
You are UDAAN AI Analytics Agent.

Analyze the founder's request and provide useful, actionable analytics.

Founder command:
{command}

Provide:
1. Key metrics or data points available from the request
2. Important observations
3. Trends or patterns
4. Problems or risks
5. Opportunities
6. Clear recommendations
7. Suggested next actions

If actual numerical data is not provided, do not invent numbers.
Clearly distinguish facts from assumptions.
Use a clear structured format.
"""

    analysis = _generate_with_gemini(prompt)

    if not analysis:
        return {
            "status": "FAILED",
            "agent": "Analytics AI",
            "message": "Analytics generation failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        ANALYTICS_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n================================\n"
            "UDAAN AI ANALYTICS\n"
            "================================\n"
        )
        file.write("Time: " + timestamp + "\n")
        file.write("Command: " + command + "\n\n")
        file.write(analysis)
        file.write("\n\n")

    return {
        "status": "SUCCESS",
        "agent": "Analytics AI",
        "command": command,
        "message": "Analytics completed successfully.",
        "output_file": ANALYTICS_OUTPUT_FILE,
        "created_at": timestamp,
        "result": analysis
    }


def analytics(command):
    return analyze(command)


def run(command):
    return analyze(command)


def execute(command):
    return analyze(command)


def process(command):
    return analyze(command)


def handle(command):
    return analyze(command)


if __name__ == "__main__":
    command = input("Analytics command: ")
    print(json.dumps(
        analyze(command),
        ensure_ascii=False,
        indent=2
    ))
