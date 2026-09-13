import importlib


class AgentRegistry:
    def __init__(self):
        self._agents = {}

    def register(self, name, module_name):
        name = str(name or "").strip()
        module_name = str(module_name or "").strip()

        if not name or not module_name:
            return False

        try:
            module = importlib.import_module(module_name)

            self._agents[name.lower()] = {
                "name": name,
                "module_name": module_name,
                "module": module,
                "status": "ACTIVE"
            }

            return True

        except Exception as error:
            self._agents[name.lower()] = {
                "name": name,
                "module_name": module_name,
                "module": None,
                "status": "ERROR",
                "error": str(error)
            }

            return False

    def unregister(self, name):
        return self._agents.pop(
            str(name or "").strip().lower(),
            None
        ) is not None

    def get(self, name):
        return self._agents.get(
            str(name or "").strip().lower()
        )

    def exists(self, name):
        return self.get(name) is not None

    def all(self):
        return list(self._agents.values())

    def active(self):
        return [
            agent
            for agent in self._agents.values()
            if agent["status"] == "ACTIVE"
        ]

    def names(self):
        return [
            agent["name"]
            for agent in self._agents.values()
        ]

    def register_defaults(self):
        agents = {
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

        for name, module_name in agents.items():
            self.register(name, module_name)

        return self.names()


registry = AgentRegistry()
registry.register_defaults()


def register_agent(name, module_name):
    return registry.register(name, module_name)


def unregister_agent(name):
    return registry.unregister(name)


def get_agent(name):
    return registry.get(name)


def get_all_agents():
    return registry.all()


def get_active_agents():
    return registry.active()


def get_agent_names():
    return registry.names()


def agent_exists(name):
    return registry.exists(name)
