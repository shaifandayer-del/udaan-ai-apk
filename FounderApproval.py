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
    description=None,
    agent=None,
    command=None,
    metadata=None,
    protected_action=None
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
        "description": description,
        "agent": agent,
        "command": command,
        "metadata": metadata,
        "protected_action": protected_action
    }

    _APPROVAL_QUEUE.append(item)
    save_approval(item)

    return item


def request_developer_build(
    command,
    title="Developer AI App Build",
    description="Developer AI wants to build an application."
):
    return request_approval(
        action="BUILD_APP",
        title=title,
        description=description,
        agent="Developer AI",
        command=command,
        protected_action=True
    )


def get_pending_approvals():
    return get_pending_approvals_db()


def approve(approval_id):
    approval = get_approval_from_db(approval_id)

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
    approval = get_approval_from_db(approval_id)

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
    return get_approval_from_db(approval_id)
