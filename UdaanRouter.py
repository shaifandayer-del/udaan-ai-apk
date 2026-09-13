from UdaanCore import execute_command


def route_command(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "message": "Command is empty."
        }

    try:
        return execute_command(command)

    except Exception as error:
        return {
            "status": "FAILED",
            "agent": "UDAAN Router",
            "message": str(error)
        }


def route(command):
    return route_command(command)


def run(command):
    return route_command(command)


def execute(command):
    return route_command(command)


def process(command):
    return route_command(command)


def handle(command):
    return route_command(command)
