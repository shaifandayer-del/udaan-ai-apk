import json
from datetime import datetime

from Orchestrator import execute_command


class UdaanCommandCenter:

    def __init__(self):
        self.status = "READY"
        self.last_command = None
        self.last_result = None

    def execute(self, command=""):
        if not command or not command.strip():
            return {
                "status": "FAILED",
                "message": "Command empty hai."
            }

        command = command.strip()

        self.status = "PROCESSING"
        self.last_command = command

        try:
            result = execute_command(command)

            if not isinstance(result, dict):
                result = {
                    "status": "SUCCESS",
                    "message": str(result)
                }

            result.setdefault("command", command)
            result.setdefault(
                "executed_at",
                datetime.now().isoformat()
            )

            self.last_result = result
            self.status = result.get("status", "UNKNOWN")

            return result

        except Exception as error:
            self.status = "FAILED"

            result = {
                "status": "FAILED",
                "command": command,
                "message": "UDAAN command execution failed.",
                "error": f"{type(error).__name__}: {error}"
            }

            self.last_result = result

            return result

    def command(self, command=""):
        return self.execute(command)

    def run(self, command=""):
        return self.execute(command)

    def process(self, command=""):
        return self.execute(command)

    def handle(self, command=""):
        return self.execute(command)

    def get_status(self):
        return {
            "status": self.status,
            "last_command": self.last_command,
            "last_result": self.last_result
        }

    def clear(self):
        self.last_command = None
        self.last_result = None
        self.status = "READY"

        return {
            "status": "SUCCESS",
            "message": "Command Center reset."
        }

    def to_json(self):
        return json.dumps(
            self.get_status(),
            ensure_ascii=False,
            default=str
        )


command_center = UdaanCommandCenter()


def run(command=""):
    return command_center.execute(command)


def execute(command=""):
    return command_center.execute(command)


def process(command=""):
    return command_center.execute(command)


def handle(command=""):
    return command_center.execute(command)


def run_agent(command=""):
    return command_center.execute(command)


def get_status():
    return command_center.get_status()


def get_command_center_status():
    return command_center.get_status()


if __name__ == "__main__":

    print(
        json.dumps(
            command_center.get_status(),
            indent=2,
            ensure_ascii=False,
            default=str
        )
    )
