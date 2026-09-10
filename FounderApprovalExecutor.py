from FounderApproval import (
    get_approval,
    approve,
    reject
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

        action = approval.get("action")
        platform = approval.get("platform")
        file_path = approval.get("file_path")

        if not action:

            return {
                "status": "FAILED",
                "message": "Action missing."
            }

        # IMPORTANT:
        # Real upload/publish integrations will be
        # connected later.
        #
        # This gate guarantees that only an APPROVED
        # request reaches the execution layer.

        return {
            "status": "APPROVED_FOR_EXECUTION",
            "approval_id":
                approval.get("approval_id"),
            "action": action,
            "platform": platform,
            "file_path": file_path,
            "message":
                "Founder approval verified. "
                "Action is ready for the real executor."
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

    from FounderApproval import request_approval

    print()
    print("=" * 60)
    print("     UDAAN AI — FOUNDER APPROVAL EXECUTOR")
    print("=" * 60)

    request = request_approval(
        action="UPLOAD_VIDEO",
        platform="YouTube",
        file_path="udaan_videos/demo.mp4",
        title="Udaan AI Demo",
        description="Founder approval test"
    )

    approval_id = request["approval_id"]

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
    print("✅ APPROVAL GATE TEST COMPLETE")
    print("=" * 60)