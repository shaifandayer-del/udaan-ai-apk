from AgentResult import success_result, failed_result, pending_result
from AgentConnector import run_agent
from UdaanCoreVisual import UdaanCoreVisual
from FounderApproval import request_approval

from UdaanDatabase import setup_database, add_task


class UdaanCore:

    def __init__(self):
        self.visual_core = UdaanCoreVisual()

    def set_visual(self, state):
        try:
            self.visual_core.set_state(state)
        except Exception:
            pass

    def find_agent(self, command):

        try:

            import SmartAgentMatcher

            functions = [
                "get_selected_agent",
                "select_agent",
                "find_agent",
                "smart_match",
                "match",
                "match_agent"
            ]

            for function_name in functions:

                function = getattr(
                    SmartAgentMatcher,
                    function_name,
                    None
                )

                if callable(function):

                    try:

                        result = function(command)

                        if result:

                            if isinstance(result, dict):

                                return (
                                    result.get("agent")
                                    or result.get("name")
                                )

                            return str(result)

                    except Exception:
                        continue

        except Exception:
            pass

        return None

    def requires_founder_approval(self, command):

        command = str(command or "").lower()

        approval_words = [

            "upload",
            "publish",
            "post",
            "deploy",
            "delete",
            "send",

            "app banao",
            "app bana",
            "android app",

            "software banao",
            "software bana",

            "website banao",
            "website bana",

            "build app",
            "build software",

            "create app",
            "create software"
        ]

        return any(
            word in command
            for word in approval_words
        )

    def create_pending_task(self, agent, command):

        try:

            setup_database()

            task_id = add_task(
                agent,
                command,
                "PENDING"
            )

            return task_id

        except TypeError:

            try:

                task_id = add_task(
                    agent,
                    command
                )

                return task_id

            except Exception:
                return None

        except Exception:
            return None

    def process(self, command):

        command = str(command or "").strip()

        if not command:

            return failed_result(
                "Main AI",
                command,
                "Command empty hai."
            )

        self.set_visual("THINKING")

        agent = self.find_agent(command)

        if not agent:

            self.set_visual("WORKING")

            return success_result(
                "Main AI",
                command,
                "Command received by Main AI."
            )

        # ==========================================
        # FOUNDER APPROVAL FLOW
        # ==========================================

        if self.requires_founder_approval(command):

            self.set_visual(
                "WAITING_APPROVAL"
            )

            # Create task BEFORE approval
            task_id = self.create_pending_task(
                agent,
                command
            )

            approval = request_approval(

                action="COMMAND_EXECUTION",

                title="UDAAN AI Founder Approval",

                description=(
                    "Founder approval required "
                    "before protected action execution."
                ),

                command=command,

                agent=agent,

                metadata={
                    "source": "UdaanCore",
                    "agent": agent,
                    "task_id": task_id
                }
            )

            return pending_result(

                agent,

                command,

                "Founder approval required. "
                "Approval ID: "
                + str(
                    approval.get("approval_id")
                )
            )

        # ==========================================
        # NORMAL AGENT EXECUTION
        # ==========================================

        self.set_visual("WORKING")

        result = run_agent(
            agent,
            command
        )

        if not isinstance(result, dict):

            result = success_result(
                agent,
                command,
                data=result
            )

        if result.get("status") == "FAILED":

            self.set_visual("ERROR")

        else:

            self.set_visual("SUCCESS")

        return result

    def get_state(self):

        try:
            return self.visual_core.get_state()

        except Exception:
            return "UNKNOWN"


_core = UdaanCore()


def process_command(command):
    return _core.process(command)


def get_core_state():
    return _core.get_state()
