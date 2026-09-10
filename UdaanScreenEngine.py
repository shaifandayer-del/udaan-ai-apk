from datetime import datetime


SCREENS = {
    "home": {
        "title": "Udaan AI",
        "icon": "🔵"
    },

    "command": {
        "title": "Command Center",
        "icon": "🧠"
    },

    "agents": {
        "title": "AI Agents",
        "icon": "🤖"
    },

    "tasks": {
        "title": "Tasks",
        "icon": "📋"
    },

    "content": {
        "title": "Content",
        "icon": "✍️"
    },

    "video": {
        "title": "Video Studio",
        "icon": "🎬"
    },

    "social": {
        "title": "Social Media",
        "icon": "📱"
    },

    "youtube": {
        "title": "YouTube",
        "icon": "▶️"
    },

    "analytics": {
        "title": "Analytics",
        "icon": "📊"
    },

    "developer": {
        "title": "Developer AI",
        "icon": "💻"
    },

    "automation": {
        "title": "Automation",
        "icon": "⚙️"
    },

    "settings": {
        "title": "Settings",
        "icon": "🔧"
    }
}


class UdaanScreenEngine:

    def __init__(self):

        self.current_screen = "home"

        self.navigation_history = []

        self.started_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def list_screens(self):

        return list(SCREENS.keys())

    def open_screen(self, screen_name):

        if screen_name not in SCREENS:

            return {
                "status": "FAILED",
                "message": "Screen not found.",
                "screen": screen_name
            }

        if self.current_screen != screen_name:

            self.navigation_history.append(
                self.current_screen
            )

        self.current_screen = screen_name

        screen = SCREENS[screen_name]

        return {
            "status": "SUCCESS",
            "screen": screen_name,
            "title": screen["title"],
            "icon": screen["icon"]
        }

    def back(self):

        if not self.navigation_history:

            self.current_screen = "home"

            return {
                "status": "SUCCESS",
                "screen": "home"
            }

        self.current_screen = self.navigation_history.pop()

        screen = SCREENS[self.current_screen]

        return {
            "status": "SUCCESS",
            "screen": self.current_screen,
            "title": screen["title"],
            "icon": screen["icon"]
        }

    def get_current_screen(self):

        screen = SCREENS[self.current_screen]

        return {
            "screen": self.current_screen,
            "title": screen["title"],
            "icon": screen["icon"]
        }


def test_engine():

    print()
    print("=" * 55)
    print("       UDAAN AI — SCREEN ENGINE TEST")
    print("=" * 55)

    engine = UdaanScreenEngine()

    print()
    print("📱 Screens:", len(engine.list_screens()))

    result = engine.open_screen("agents")

    print(
        result["icon"],
        result["title"],
        "->",
        result["status"]
    )

    result = engine.open_screen("video")

    print(
        result["icon"],
        result["title"],
        "->",
        result["status"]
    )

    result = engine.back()

    print(
        "↩️ Back ->",
        result["title"]
    )

    print()
    print("📍 Current screen:")

    print(
        engine.get_current_screen()
    )

    print()
    print("=" * 55)
    print("✅ SCREEN ENGINE READY")
    print("=" * 55)


if __name__ == "__main__":
    test_engine()