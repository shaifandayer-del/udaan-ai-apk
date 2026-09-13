import datetime
import json
import os


HISTORY_FILE = "udaan_history.json"


class UdaanHistory:
    def __init__(self, history_file=HISTORY_FILE):
        self.history_file = history_file
        self.history = self._load()

    def _load(self):
        if not os.path.exists(self.history_file):
            return []

        try:
            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except Exception:
            return []

    def _save(self):
        with open(
            self.history_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.history,
                file,
                ensure_ascii=False,
                indent=2
            )

    def add(
        self,
        command,
        agent=None,
        status="UNKNOWN",
        result=None
    ):
        command = str(command or "").strip()

        if not command:
            return False

        entry = {
            "command": command,
            "agent": agent,
            "status": status,
            "result": result,
            "created_at":
                datetime.datetime.now().isoformat()
        }

        self.history.append(entry)

        self.history = self.history[-500:]

        self._save()

        return True

    def get_recent(self, limit=20):
        try:
            limit = max(1, int(limit))
        except Exception:
            limit = 20

        return self.history[-limit:]

    def get_all(self):
        return list(self.history)

    def search(self, query):
        query = str(query or "").strip().lower()

        if not query:
            return []

        return [
            item
            for item in self.history
            if query in str(
                item.get("command", "")
            ).lower()
        ]

    def clear(self):
        self.history = []
        self._save()
        return True


history = UdaanHistory()


def add_history(
    command,
    agent=None,
    status="UNKNOWN",
    result=None
):
    return history.add(
        command,
        agent,
        status,
        result
    )


def get_recent_history(limit=20):
    return history.get_recent(limit)


def get_history():
    return history.get_all()


def search_history(query):
    return history.search(query)


def clear_history():
    return history.clear()
