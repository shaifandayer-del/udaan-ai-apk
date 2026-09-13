import datetime
import json
import os


MEMORY_FILE = "udaan_memory.json"


class UdaanMemory:
    def __init__(self, memory_file=MEMORY_FILE):
        self.memory_file = memory_file
        self.memory = self._load()

    def _load(self):
        if not os.path.exists(self.memory_file):
            return {
                "founder": {},
                "commands": [],
                "preferences": {},
                "facts": {}
            }

        try:
            with open(
                self.memory_file,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

        return {
            "founder": {},
            "commands": [],
            "preferences": {},
            "facts": {}
        }

    def _save(self):
        with open(
            self.memory_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.memory,
                file,
                ensure_ascii=False,
                indent=2
            )

    def remember(self, key, value):
        key = str(key or "").strip()

        if not key:
            return False

        self.memory["facts"][key] = {
            "value": value,
            "updated_at": datetime.datetime.now().isoformat()
        }

        self._save()
        return True

    def recall(self, key):
        key = str(key or "").strip()

        item = self.memory["facts"].get(key)

        if not item:
            return None

        return item.get("value")

    def set_preference(self, key, value):
        key = str(key or "").strip()

        if not key:
            return False

        self.memory["preferences"][key] = {
            "value": value,
            "updated_at": datetime.datetime.now().isoformat()
        }

        self._save()
        return True

    def get_preference(self, key):
        item = self.memory["preferences"].get(
            str(key or "").strip()
        )

        if not item:
            return None

        return item.get("value")

    def set_founder(self, key, value):
        key = str(key or "").strip()

        if not key:
            return False

        self.memory["founder"][key] = value

        self._save()
        return True

    def get_founder(self, key):
        return self.memory["founder"].get(
            str(key or "").strip()
        )

    def remember_command(
        self,
        command,
        agent=None,
        result=None
    ):
        command = str(command or "").strip()

        if not command:
            return False

        self.memory["commands"].append({
            "command": command,
            "agent": agent,
            "result": result,
            "created_at":
                datetime.datetime.now().isoformat()
        })

        self.memory["commands"] = self.memory[
            "commands"
        ][-100:]

        self._save()
        return True

    def get_recent_commands(self, limit=20):
        try:
            limit = max(1, int(limit))
        except Exception:
            limit = 20

        return self.memory["commands"][-limit:]

    def get_all(self):
        return self.memory

    def clear(self):
        self.memory = {
            "founder": {},
            "commands": [],
            "preferences": {},
            "facts": {}
        }

        self._save()
        return True


memory = UdaanMemory()


def remember(key, value):
    return memory.remember(key, value)


def recall(key):
    return memory.recall(key)


def set_preference(key, value):
    return memory.set_preference(key, value)


def get_preference(key):
    return memory.get_preference(key)


def set_founder(key, value):
    return memory.set_founder(key, value)


def get_founder(key):
    return memory.get_founder(key)


def remember_command(command, agent=None, result=None):
    return memory.remember_command(
        command,
        agent,
        result
    )


def get_recent_commands(limit=20):
    return memory.get_recent_commands(limit)


def get_memory():
    return memory.get_all()


def clear_memory():
    return memory.clear()
