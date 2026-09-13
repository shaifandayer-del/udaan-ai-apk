SessionManager.py

import datetime
import uuid


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, founder="Founder"):
        session_id = str(uuid.uuid4())

        session = {
            "session_id": session_id,
            "founder": str(founder or "Founder"),
            "status": "ACTIVE",
            "created_at": datetime.datetime.now().isoformat(),
            "last_activity": datetime.datetime.now().isoformat()
        }

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id):
        return self.sessions.get(str(session_id))

    def update_activity(self, session_id):
        session = self.get_session(session_id)

        if not session:
            return {
                "status": "FAILED",
                "message": "Session not found."
            }

        session["last_activity"] = datetime.datetime.now().isoformat()
        return session

    def close_session(self, session_id):
        session = self.get_session(session_id)

        if not session:
            return {
                "status": "FAILED",
                "message": "Session not found."
            }

        session["status"] = "CLOSED"
        session["closed_at"] = datetime.datetime.now().isoformat()

        return session

    def get_active_sessions(self):
        return [
            session
            for session in self.sessions.values()
            if session["status"] == "ACTIVE"
        ]

    def get_all_sessions(self):
        return list(self.sessions.values())


session_manager = SessionManager()


def create_session(founder="Founder"):
    return session_manager.create_session(founder)


def get_session(session_id):
    return session_manager.get_session(session_id)


def update_activity(session_id):
    return session_manager.update_activity(session_id)


def close_session(session_id):
    return session_manager.close_session(session_id)


def get_active_sessions():
    return session_manager.get_active_sessions()


def get_all_sessions():
    return session_manager.get_all_sessions()
