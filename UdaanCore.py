from AgentResult import (
    success_result,
    failed_result,
    pending_result
)

from AgentConnector import run_agent
from UdaanCoreVisual import UdaanCoreVisual


class UdaanCore:

    def __init__(self):
        self.visual_core = UdaanCoreVisual()

    def set_visual(self, state):

        result = self.visual_core.set_state(state)

        print(
            "🔵 CORE:",
            result.get("state"),
            "|",
            result.get("label")
        )

    def find_agent(self, command):

        try:

            import SmartAgentMatcher

            possible_functions = [
                "get_selected_agent",
                "select_agent",
                "find_agent",
                "smart_match",
                "match",
                "match_agent"
            ]

            for function_name in possible_functions:

                function = getattr(
                    SmartAgentMatcher,
                    function_name,
                    None
                )

                if callable(function):

                    try:
                        result = function(command)

                        if result:
                            return result

                    except Exception:
                        continue

            return None

        except Exception as error:

            print(
                "⚠️ Smart Agent Matcher unavailable:",
                error
            )

            return None

    def process(self, command):

        if not command or not command.strip():

            self.set_visual("ERROR")

            return failed_result(
                "Main AI",
                command,
                "Command empty hai."
            )

        command = command.strip()

        try:

            self.set_visual("THINKING")

            agent = self.find_agent(command)

            if not agent:

                self.set_visual("WORKING")

                result = success_result(
                    "Main AI",
                    command,
                    "Main AI command received and ready."
                )

                self.set_visual("SUCCESS")

                return result

            approval_words = [
                "upload",
                "publish",
                "post",
                "deploy",
                "delete",
                "send"
            ]

            requires_approval = any(
                word in command.lower()
                for word in approval_words
            )

            if requires_approval:

                self.set_visual("WAITING_APPROVAL")

                return pending_result(
                    agent,
                    command,
                    "Founder approval required before execution."
                )

            self.set_visual("WORKING")

            result = run_agent(
                agent,
                command
            )

            if not isinstance(result, dict):

                self.set_visual("ERROR")

                return failed_result(
                    agent,
                    command,
                    "Invalid agent response."
                )

            if result.get("status") == "FAILED":

                self.set_visual("ERROR")

            else:

                self.set_visual("SUCCESS")

            return result

        except Exception as error:

            self.set_visual("ERROR")

            return failed_result(
                "Main AI",
                command,
                "Core processing failed.",
                str(error)
            )


_core = UdaanCore()


def process_command(command):
    return _core.process(command)


def get_core_state():
    return _core.visual_core.get_state()


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — CORE VISUAL TEST")
    print("=" * 60)

    commands = [
        "research latest AI trends",
        "create YouTube content",
        "upload video to YouTube"
    ]

    for command in commands:

        print()
        print("🗣️", command)

        result = process_command(command)

        print("📊 Status :", result.get("status"))
        print("🤖 Agent  :", result.get("agent"))
        print("💬 Message:", result.get("message"))

    print()
    print("🔵 Final Core State:")
    print(get_core_state())

    print()
    print("✅ CORE VISUAL INTEGRATION READY")