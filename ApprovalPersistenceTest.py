from ApprovalDatabase import (
    save_approval,
    get_approval,
    get_pending_approvals,
    update_approval_status,
    delete_approval
)


def run_test():
    approval = {
        "approval_id": "test-approval-001",
        "action": "TEST_ACTION",
        "agent": "Developer",
        "platform": "UDAAN",
        "file_path": None,
        "title": "Approval Persistence Test",
        "description": "Testing approval database persistence.",
        "status": "PENDING"
    }

    save_approval(approval)

    saved = get_approval(
        approval["approval_id"]
    )

    if not saved:
        return {
            "success": False,
            "message": "Approval was not saved."
        }

    if saved["status"] != "PENDING":
        return {
            "success": False,
            "message": "Initial approval status is invalid."
        }

    update_approval_status(
        approval["approval_id"],
        "APPROVED",
        result="Test approval successful."
    )

    updated = get_approval(
        approval["approval_id"]
    )

    if not updated:
        return {
            "success": False,
            "message": "Approval disappeared after update."
        }

    if updated["status"] != "APPROVED":
        return {
            "success": False,
            "message": "Approval status update failed."
        }

    pending = get_pending_approvals()

    if any(
        item["approval_id"]
        == approval["approval_id"]
        for item in pending
    ):
        return {
            "success": False,
            "message": "Approved item still appears as pending."
        }

    delete_approval(
        approval["approval_id"]
    )

    deleted = get_approval(
        approval["approval_id"]
    )

    if deleted is not None:
        return {
            "success": False,
            "message": "Approval deletion failed."
        }

    return {
        "success": True,
        "status": "PASSED",
        "message": "Approval persistence test passed."
    }


if __name__ == "__main__":
    print(run_test())
