from UdaanCore import process_command, get_core_state


class UdaanCommandCenter:

    def __init__(self):
        self.name = "Udaan AI Command Center"

    def execute(self, command):

        if not command or not command.strip():

            return {
                "status": "FAILED",
                "message": "Command empty hai.",
                "core_state": get_core_state()
            }

        result = process_command(command)

        result["core_state"] = get_core_state()

        return result

    def status(self):

        return {
            "system": self.name,
            "core_state": get_core_state(),
            "status": "ONLINE"
        }


_center = UdaanCommandCenter()


def execute_command(command):

    return _center.execute(command)


def get_command_center_status():

    return _center.status()


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("          UDAAN AI COMMAND CENTER")
    print("=" * 60)

    print()
    print("🟢 System Status:")
    print(get_command_center_status())

    print()
    command = "research latest AI trends"

    print("🗣️ Command:", command)

    result = execute_command(command)

    print()
    print("📊 Result:")
    print(result)

    print()
    print("=" * 60)
    print("✅ COMMAND CENTER READY")
    print("=" * 60)