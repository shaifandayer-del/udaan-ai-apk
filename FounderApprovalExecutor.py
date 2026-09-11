# ==========================================
# UDAAN AI - FOUNDER APPROVAL EXECUTOR
# STEP 98
# ==========================================

from FounderApproval import (
    get_approval,
    approve,
    reject
)

from ApprovalExecutor import (
    execute_approved_action
)


class FounderApprovalExecutor:

    def approve_request(self, approval_id):

        result = approve(approval_id)

        if result.get("status") != "APPROVED":

            return result

        approval = result.get("approval")

        if not approval:

            return {
                "status": "FAILED",
                "message": "Approval data missing."
            }

        return self.execute_approved_action(
            approval
        )

    def reject_request(self, approval_id):

        return reject(approval_id)

    def execute_approved_action(self, approval):

        approval_status = approval.get(
            "status"
        )

        if approval_status != "APPROVED":

            return {
                "status": "FAILED",
                "message": (
                    "Only APPROVED requests "
                    "can be executed."
                )
            }

        action = approval.get("action")
        platform = approval.get("platform")
        file_path = approval.get("file_path")
        command = approval.get("command")

        if not action:

            return {
                "status": "FAILED",
                "message": "Action missing."
            }

        # --------------------------------------
        # COMMAND REQUIRED
        # --------------------------------------

        if not command:

            return {
                "status": "FAILED",
                "approval_id": approval.get(
                    "approval_id"
                ),
                "action": action,
                "message": (
                    "Approved action has no "
                    "execution command."
                )
            }

        # --------------------------------------
        # REAL APPROVED EXECUTION
        # --------------------------------------

        try:

            result = execute_approved_action(
                approval.get(
                    "agent",
                    "Main AI"
                ),
                command
            )

            return {
                "status": "EXECUTED",
                "approval_id": approval.get(
                    "approval_id"
                ),
                "action": action,
                "platform": platform,
                "file_path": file_path,
                "command": command,
                "result": result,
                "message": (
                    "Founder approval verified "
                    "and approved action sent "
                    "to execution layer."
                )
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "approval_id": approval.get(
                    "approval_id"
                ),
                "action": action,
                "message": (
                    "Approved action execution failed."
                ),
                "error": str(error)
            }


_executor = FounderApprovalExecutor()


def approve_and_execute(approval_id):

    return _executor.approve_request(
        approval_id
    )


def reject_request(approval_id):

    return _executor.reject_request(
        approval_id
    )


if __name__ == "__main__":

    from FounderApproval import (
        request_approval
    )

    print()
    print("=" * 60)
    print("     UDAAN AI — FOUNDER APPROVAL EXECUTOR")
    print("=" * 60)

    request = request_approval(
        action="UPLOAD_VIDEO",
        platform="YouTube",
        file_path="udaan_videos/demo.mp4",
        title="Udaan AI Demo",
        description="Founder approval test",
        command="YouTube ke liye video publish karo",
        metadata={
            "source": "Founder Approval Test"
        }
    )

    approval_id = request[
        "approval_id"
    ]

    print()
    print("🆔 Approval ID:", approval_id)
    print("⏳ Status:", request["status"])

    print()
    print("👤 Founder approving...")

    result = approve_and_execute(
        approval_id
    )

    print()
    print("📊 Result:")
    print(result)

    print()
    print("=" * 60)
    print("✅ APPROVAL EXECUTION BRIDGE READY")
    print("=" * 60)
