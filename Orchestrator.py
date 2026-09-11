# ==========================================
# UDAAN AI - ORCHESTRATOR
# Compatibility Layer
# ==========================================

from UdaanCore import (
    process_command,
    get_core_state
)


class Orchestrator:

    def __init__(self):
        self.name = "UDAAN AI Orchestrator"

    def route_command(self, command):
        result = process_command(command)

        return result.get(
            "agent",
            "Main AI"
        )

    def execute(self, command):
        command = str(command).strip()

        if not command:
            return {
                "status": "FAILED",
                "message": "Founder command empty hai."
            }

        result = process_command(command)

        return {
            "status": result.get(
                "status",
                "FAILED"
            ),
            "founder_command": command,
            "assigned_agent": result.get(
                "agent",
                "Main AI"
            ),
            "result": result,
            "core_state": get_core_state()
        }


def create_orchestrator():
    return Orchestrator()


if __name__ == "__main__":

    print("=" * 60)
    print("          UDAAN AI ORCHESTRATOR")
    print("=" * 60)

    orchestrator = create_orchestrator()

    command = input(
        "\nUDAAN command: "
    ).strip()

    result = orchestrator.execute(command)

    print("\nRESULT:")
    print(result)
