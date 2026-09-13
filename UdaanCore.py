
import datetime
import json

from CommandParser import parse_command
from TaskManager import (
    create_task,
    start_task,
    complete_task,
    fail_task
)
from AgentConnector import execute_agent


class UdaanCore:
    def __init__(self):
        self.name = "UDAAN AI"

    def execute_command(self, command):
        command = str(command or "").strip()

        if not command:
            return {
                "status": "FAILED",
                "agent": "UDAAN Core",
                "message": "Command is empty."
            }

        try:
            parsed = parse_command(command)

            if parsed.get("status") != "SUCCESS":
                return parsed

            agent = parsed.get("agent", "Main AI")
            task_command = parsed.get("command", command)

            task = create_task(
                task_command,
                agent
            )

            if task.get("status") == "FAILED":
                return task

            task_id = task["task_id"]

            start_task(task_id)

            result = execute_agent(
                agent,
                task_command
            )

            if isinstance(result, dict):
                if result.get("status") == "SUCCESS":
                    complete_task(
                        task_id,
                        result
                    )

                    return {
                        "status": "SUCCESS",
                        "agent": agent,
                        "task_id": task_id,
                        "intent": parsed.get("intent"),
                        "command": task_command,
                        "result": result,
                        "created_at":
                            datetime.datetime.now().isoformat()
                    }

                fail_task(
                    task_id,
                    result.get(
                        "message",
                        "Agent execution failed."
                    )
                )

                return {
                    "status": "FAILED",
                    "agent": agent,
                    "task_id": task_id,
                    "intent": parsed.get("intent"),
                    "command": task_command,
                    "result": result,
                    "created_at":
                        datetime.datetime.now().isoformat()
                }

            fail_task(
                task_id,
                "Agent returned invalid result."
            )

            return {
                "status": "FAILED",
                "agent": agent,
                "task_id": task_id,
                "message": "Agent returned invalid result."
            }

        except Exception as error:
            return {
                "status": "FAILED",
                "agent": "UDAAN Core",
                "message": str(error),
                "created_at":
                    datetime.datetime.now().isoformat()
            }


core = UdaanCore()


def execute_command(command):
    return core.execute_command(command)


def run(command):
    return core.execute_command(command)


def execute(command):
    return core.execute_command(command)


def process(command):
    return core.execute_command(command)


def handle(command):
    return core.execute_command(command)


if __name__ == "__main__":
    command = input("UDAAN Command: ")

    print(
        json.dumps(
            core.execute_command(command),
            ensure_ascii=False,
            indent=2
        )
    )
