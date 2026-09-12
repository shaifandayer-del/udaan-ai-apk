import importlib
from datetime import datetime


class UdaanFinalIntegration:

    def __init__(self):
        self.status = "READY"
        self.last_result = None

    def _load(self, module_name):
        try:
            return importlib.import_module(module_name)
        except Exception as error:
            return None, f"{type(error).__name__}: {error}"

    def _call(self, module, functions, command):
        for name in functions:
            function = getattr(module, name, None)

            if not callable(function):
                continue

            try:
                result = function(command)

                if isinstance(result, dict):
                    return result

                return {
                    "status": "SUCCESS",
                    "message": str(result)
                }

            except TypeError:
                try:
                    result = function()

                    if isinstance(result, dict):
                        return result

                    return {
                        "status": "SUCCESS",
                        "message": str(result)
                    }

                except Exception as error:
                    return {
                        "status": "FAILED",
                        "error": f"{type(error).__name__}: {error}"
                    }

            except Exception as error:
                return {
                    "status": "FAILED",
                    "error": f"{type(error).__name__}: {error}"
                }

        return {
            "status": "FAILED",
            "message": "Required function nahi mili."
        }

    def execute(self, command=""):
        if not command or not command.strip():
            return {
                "status": "FAILED",
                "message": "Command empty hai."
            }

        command = command.strip()
        self.status = "PROCESSING"

        module, error = self._load("UdaanCommandCenter")

        if module is None:
            self.status = "FAILED"

            return {
                "status": "FAILED",
                "stage": "COMMAND_CENTER",
                "message": "UdaanCommandCenter load nahi hua.",
                "error": error
            }

        result = self._call(
            module,
            [
                "execute",
                "run",
                "process",
                "handle",
                "run_agent"
            ],
            command
        )

        result.setdefault("command", command)
        result.setdefault(
            "executed_at",
            datetime.now().isoformat()
        )

        self.last_result = result
        self.status = result.get("status", "UNKNOWN")

        return result

    def run(self, command=""):
        return self.execute(command)

    def process(self, command=""):
        return self.execute(command)

    def handle(self, command=""):
        return self.execute(command)

    def run_agent(self, command=""):
        return self.execute(command)

    def get_status(self):
        return {
            "status": self.status,
            "last_result": self.last_result
        }


integration = UdaanFinalIntegration()


def execute(command=""):
    return integration.execute(command)


def run(command=""):
    return integration.execute(command)


def process(command=""):
    return integration.execute(command)


def handle(command=""):
    return integration.execute(command)


def run_agent(command=""):
    return integration.execute(command)


def get_status():
    return integration.get_status()


if __name__ == "__main__":
    print(integration.get_status())
