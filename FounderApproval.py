# ==========================================
# UDAAN AI - FOUNDER APPROVAL
# STEP 96
# Persistent Approval + Developer Build
# ==========================================

import time

from ApprovalDatabase import (
    save_approval,
    update_approval_status,
    get_approval_from_db,
    get_pending_approvals_db
)


_APPROVAL_QUEUE = []


PROTECTED_ACTIONS = {
    "UPLOAD_VIDEO",
    "UPLOAD_YOUTUBE",
    "UPLOAD_INSTAGRAM",
    "PUBLISH_CONTENT",
    "BUILD_APP",
    "BUILD_SOFTWARE",
    "DEPLOY_APP",
    "DEPLOY_SOFTWARE",
    "DELETE_PROJECT",
}


def request_approval(
    action,
    platform=None,
    file_path=None,
    title=None,
    description=None,
    command=None,
    metadata=None
):

    action = str(action).strip().upper()

    approval_id = "APR-" + str(
        int(time.time() * 1000)
    )

    item = {
        "approval_id": approval_id,
        "status": "PENDING",
        "action": action,
        "platform": platform,
        "file_path": file_path,
        "title": title,
        "description": description,
        "command": command,
        "metadata": metadata or {},
        "protected_action": (
            action in PROTECTED_ACTIONS
        )
    }

    _APPROVAL_QUEUE.append(item)

    # Persistent database save
    save_approval(item)

    return item


def request_developer_build(
    command,
    project_name=None,
    description=None
):
    """
    Developer AI ke app/software build request
    ko Founder Approval queue mein bhejta hai.

    Actual build approval ke baad hi external
    execution layer se kiya jayega.
    """

    if not command or not str(command).strip():

        return {
            "status": "FAILED",
            "message": "Developer build command empty hai."
        }

    return request_approval(
        action="BUILD_APP",
        platform="Android",
        title=project_name or "UDAAN Generated App",
        description=(
            description
            or "Developer AI app build request."
        ),
        command=str(command).strip(),
        metadata={
            "source": "Developer AI",
            "build_type": "application"
        }
    )


def get_pending_approvals():

    # Database is the persistent source
    return get_pending_approvals_db()


def approve(approval_id):

    approval = get_approval_from_db(
        approval_id
    )

    if not approval:

        return {
            "status": "FAILED",
            "message": "Approval ID not found."
        }

    if approval["status"] != "PENDING":

        return {
            "status": "FAILED",
            "message": "Approval already processed.",
            "approval": approval
        }

    updated = update_approval_status(
        approval_id,
        "APPROVED"
    )

    if not updated:

        return {
            "status": "FAILED",
            "message": "Database update failed."
        }

    approval["status"] = "APPROVED"

    return {
        "status": "APPROVED",
        "approval": approval
    }


def reject(approval_id):

    approval = get_approval_from_db(
        approval_id
    )

    if not approval:

        return {
            "status": "FAILED",
            "message": "Approval ID not found."
        }

    if approval["status"] != "PENDING":

        return {
            "status": "FAILED",
            "message": "Approval already processed.",
            "approval": approval
        }

    updated = update_approval_status(
        approval_id,
        "REJECTED"
    )

    if not updated:

        return {
            "status": "FAILED",
            "message": "Database update failed."
        }

    approval["status"] = "REJECTED"

    return {
        "status": "REJECTED",
        "approval": approval
    }


def get_approval(approval_id):

    return get_approval_from_db(
        approval_id
    )


def is_protected_action(action):

    return str(action).strip().upper() in PROTECTED_ACTIONS


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — PERSISTENT APPROVAL TEST")
    print("=" * 60)

    request = request_approval(
        action="UPLOAD_VIDEO",
        platform="YouTube",
        file_path="udaan_videos/demo.mp4",
        title="Udaan AI Demo",
        description="Persistent approval test"
    )

    print()
    print("🆔 Approval ID:")
    print(request["approval_id"])

    print()
    print("📊 Initial Status:")
    print(request["status"])

    print()
    print("💾 Saved to database.")

    print()
    print("📋 Pending Approvals:")

    print(
        get_pending_approvals()
    )

    print()
    print("👤 Founder approving...")

    result = approve(
        request["approval_id"]
    )

    print()
    print("📊 Approval Result:")
    print(result)

    print()
    print("🔎 Database Record:")

    print(
        get_approval(
            request["approval_id"]
        )
    )

    print()
    print("=" * 60)
    print("✅ PERSISTENT APPROVAL SYSTEM READY")
    print("=" * 60)
