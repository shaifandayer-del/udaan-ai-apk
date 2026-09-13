AgentManager.py

import importlib
import datetime


class AgentManager:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, module_name):
        name = str(name or "").strip()
        module_name = str(module_name or "").strip()

        if not name or not module_name:
            return False

        try:
            module = importlib.import_module(module_name)
            self.agents[name.lower()] = {
                "name": name,
                "module": module,
                "status": "ACTIVE"
            }
            return True
        except Exception as error:
            self.agents[name.lower()] = {
                "name": name,
                "module": None,
                "status": "ERROR",
                "error": str(error)
            }
            return False

    def load_default_agents(self):
        agent_modules = {
            "Research": "Research",
            "Content": "Content",
            "Video": "Video",
            "YouTube": "YouTube",
            "Social": "Social",
            "Analytics": "Analytics",
            "Marketing": "Marketing",
            "Developer": "Developer",
            "Automation": "Automation",
            "Creative": "Creative"
        }

        for name, module_name in agent_modules.items():
            self.register_agent(name, module_name)

        return self.get_agents()

    def get_agents(self):
        return [
            {
                "name": data["name"],
                "status": data["status"]
            }
            for data in self.agents.values()
        ]

    def get_agent(self, name):
        return self.agents.get(
            str(name or "").strip().lower()
        )

    def execute(self, name, command):
        agent = self.get_agent(name)

        if not agent:
            return {
                "status": "FAILED",
                "agent": str(name),
                "message": "Agent not found."
            }

        if agent["module"] is None:
            return {
                "status": "FAILED",
                "agent": agent["name"],
                "message": agent.get(
                    "error",
                    "Agent could not be loaded."
                )
            }

        module = agent["module"]

        for function_name in (
            "run",
            "execute",
            "process",
            "handle"
        ):
            function = getattr(
                module,
                function_name,
                None
            )

            if callable(function):
                try:
                    result = function(command)

                    if isinstance(result, dict):
                        return result

                    return {
                        "status": "SUCCESS",
                        "agent": agent["name"],
                        "result": result
                    }

                except Exception as error:
                    return {
                        "status": "FAILED",
                        "agent": agent["name"],
                        "message": str(error),
                        "created_at":
                            datetime.datetime.now().isoformat()
                    }

        return {
            "status": "FAILED",
            "agent": agent["name"],
            "message": "No executable function found."
        }


_manager = AgentManager()
_manager.load_default_agents()


def get_agent_manager():
    return _manager


def get_agents():
    return _manager.get_agents()


def execute_agent(name, command):
    return _manager.execute(name, command)


def run_agent(name, command):
    return _manager.execute(name, command)


def register_agent(name, module_name):
    return _manager.register_agent(
        name,
        module_name
    )


if __name__ == "__main__":
    print(_manager.get_agents())
