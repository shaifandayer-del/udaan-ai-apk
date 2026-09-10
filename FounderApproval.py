# FounderApproval.py

import time

from ApprovalDatabase import (
    save_approval,
    update_approval_status,
    get_approval_from_db,
    get_pending_approvals_db
)


_APPROVAL_QUEUE = []


def request_approval(
    action,
    platform=None,
    file_path=None,
    title=None,
    description=None
):

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
        "description": description
    }

    _APPROVAL_QUEUE.append(item)

    # Persistent database save
    save_approval(item)

    return item


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