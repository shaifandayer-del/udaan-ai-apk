from UdaanCore import process_command
from FounderApproval import (
    request_approval,
    get_pending_approvals,
    get_approval,
)


PROTECTED_WORDS = [
    "upload",
    "publish",
    "post",
    "deploy",
    "delete",
    "send",
    "app banao",
    "app bana",
    "software banao",
    "software bana",
    "build app",
    "build software",
    "create app",
    "create software",
]


def requires_founder_approval(command):

    if not command:
        return False

    text = command.lower()

    return any(
        word in text
        for word in PROTECTED_WORDS
    )


def submit_command(
    command,
    agent=None,
    platform=None,
    action="COMMAND_EXECUTION",
):

    if not command or not command.strip():

        return {
            "status": "FAILED",
            "message": "Command empty hai."
        }

    command = command.strip()

    if requires_founder_approval(command):

        approval = request_approval(
            action=action,
            platform=platform,
            title="UDAAN AI Founder Approval",
            description=(
                "Founder approval required "
                "before protected action execution."
            ),
            command=command,
            agent=agent,
            metadata={
                "source": "ApprovalApi",
                "protected": True,
            },
        )

        return {
            "status": "PENDING_APPROVAL",
            "command": command,
            "approval_id": approval.get("approval_id"),
            "agent": agent,
            "message": "Founder approval required.",
            "next_action": "approve_or_reject",
        }

    return process_command(command)


def approval_status(approval_id):

    approval = get_approval(approval_id)

    if not approval:

        return {
            "status": "FAILED",
            "message": "Approval ID not found.",
            "approval_id": approval_id,
        }

    return {
        "status": approval.get("status"),
        "approval": approval,
    }


def pending_approvals():

    return {
        "status": "SUCCESS",
        "approvals": get_pending_approvals(),
    }


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — FOUNDER APPROVAL API")
    print("=" * 60)

    tests = [
        "research latest AI trends",
        "create a video",
        "upload video to YouTube",
        "publish Instagram post",
        "build Android app",
    ]

    for command in tests:

        print()
        print("🗣️", command)

        result = submit_command(command)

        print("📊 Status :", result.get("status"))
        print("💬 Message:", result.get("message"))

        if result.get("approval_id"):
            print(
                "🔐 Approval ID:",
                result.get("approval_id")
            )

    print()
    print("=" * 60)
    print("✅ FOUNDER APPROVAL API READY")
    print("=" * 60)
