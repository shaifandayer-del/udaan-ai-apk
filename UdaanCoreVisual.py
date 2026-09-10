from datetime import datetime


CORE_STATES = {

    "IDLE": {
        "label": "Ready",
        "animation": "slow_pulse",
        "intensity": 0.30
    },

    "THINKING": {
        "label": "Thinking",
        "animation": "rotation",
        "intensity": 0.60
    },

    "WORKING": {
        "label": "Working",
        "animation": "energy_flow",
        "intensity": 0.90
    },

    "SUCCESS": {
        "label": "Success",
        "animation": "bright_pulse",
        "intensity": 1.00
    },

    "ERROR": {
        "label": "Error",
        "animation": "warning_pulse",
        "intensity": 0.80
    },

    "WAITING_APPROVAL": {
        "label": "Founder Approval",
        "animation": "attention_pulse",
        "intensity": 0.70
    }
}


class UdaanCoreVisual:

    def __init__(self):

        self.state = "IDLE"

        self.updated_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def set_state(self, state):

        state = state.upper()

        if state not in CORE_STATES:

            return {
                "status": "FAILED",
                "message": "Invalid core state.",
                "state": state
            }

        self.state = state

        self.updated_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        configuration = CORE_STATES[state]

        return {
            "status": "SUCCESS",
            "state": state,
            "label": configuration["label"],
            "animation": configuration["animation"],
            "intensity": configuration["intensity"],
            "updated_at": self.updated_at
        }

    def get_state(self):

        configuration = CORE_STATES[self.state]

        return {
            "state": self.state,
            "label": configuration["label"],
            "animation": configuration["animation"],
            "intensity": configuration["intensity"],
            "updated_at": self.updated_at
        }


def test_visual_core():

    print()
    print("=" * 60)
    print("        UDAAN AI — CORE VISUAL STATE TEST")
    print("=" * 60)

    core = UdaanCoreVisual()

    states = [
        "IDLE",
        "THINKING",
        "WORKING",
        "WAITING_APPROVAL",
        "SUCCESS",
        "ERROR"
    ]

    print()

    for state in states:

        result = core.set_state(state)

        print(
            "🔵",
            result["state"],
            "|",
            result["label"],
            "|",
            result["animation"],
            "|",
            result["intensity"]
        )

    print()
    print("📍 Final State:")

    print(core.get_state())

    print()
    print("=" * 60)
    print("✅ CORE VISUAL ENGINE READY")
    print("=" * 60)


if __name__ == "__main__":
    test_visual_core()