import datetime
import json

from GeminiBrain import ask_gemini
from AgentConnector import execute_agent


def main_ai(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Main AI",
            "message": "Command is empty."
        }

    prompt = f"""
You are the Main AI / Orchestrator of UDAAN AI.

Founder command:
{command}

Identify the best specialized UDAAN AI agent for this command.

Available agents:
Research
Content
Video
YouTube
Social
Analytics
Marketing
Developer
Automation
Creative

Return ONLY valid JSON:
{{
    "agent": "AgentName",
    "task": "clear task for that agent"
}}
"""

    try:
        decision_text = ask_gemini(prompt)

        if not decision_text:
            return {
                "status": "FAILED",
                "agent": "Main AI",
                "message": "Main AI could not determine the required agent."
            }

        decision_text = decision_text.strip()

        if decision_text.startswith("```"):
            decision_text = decision_text.replace("```json", "")
            decision_text = decision_text.replace("```", "").strip()

        decision = json.loads(decision_text)

        agent_name = str(
            decision.get("agent", "")
        ).strip()

        task = str(
            decision.get("task", command)
        ).strip()

        if not agent_name:
            return {
                "status": "FAILED",
                "agent": "Main AI",
                "message": "No suitable agent was selected."
            }

        result = execute_agent(
            agent_name,
            task
        )

        return {
            "status": result.get("status", "FAILED")
            if isinstance(result, dict)
            else "FAILED",
            "agent": "Main AI",
            "selected_agent": agent_name,
            "task": task,
            "result": result,
            "created_at": datetime.datetime.now().isoformat()
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "agent": "Main AI",
            "message": str(error)
        }


def run(command):
    return main_ai(command)


def execute(command):
    return main_ai(command)


def process(command):
    return main_ai(command)


def handle(command):
    return main_ai(command)


if __name__ == "__main__":
    command = input("UDAAN AI Command: ")
    print(json.dumps(
        main_ai(command),
        ensure_ascii=False,
        indent=2
    ))
