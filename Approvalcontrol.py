import datetime
from ApprovalQueue import (
    approval_queue
)


class ApprovalControl:

    def pending(self):
        return approval_queue.get_pending()

    def get(self, approval_id):
        return approval_queue.get(approval_id)

    def approve(self, approval_id):
        item = approval_queue.approve(approval_id)

        if not item:
            return {
                "success": False,
                "status": "NOT_FOUND",
                "approval_id": approval_id
            }

        item["approved_at"] = (
            datetime.datetime.now().isoformat()
        )

        return {
            "success": True,
            "status": "APPROVED",
            "approval": item
        }

    def reject(self, approval_id):
        item = approval_queue.reject(approval_id)

        if not item:
            return {
                "success": False,
                "status": "NOT_FOUND",
                "approval_id": approval_id
            }

        item["rejected_at"] = (
            datetime.datetime.now().isoformat()
        )

        return {
            "success": True,
            "status": "REJECTED",
            "approval": item
        }

    def complete(self, approval_id, result=None):
        item = approval_queue.complete(
            approval_id,
            result
        )

        if not item:
            return {
                "success": False,
                "status": "NOT_FOUND",
                "approval_id": approval_id
            }

        return {
            "success": True,
            "status": "COMPLETED",
            "approval": item
        }

    def fail(self, approval_id, error=None):
        item = approval_queue.fail(
            approval_id,
            error
        )

        if not item:
            return {
                "success": False,
                "status": "NOT_FOUND",
                "approval_id": approval_id
            }

        return {
            "success": False,
            "status": "FAILED",
            "approval": item
        }

    def summary(self):
        all_items = approval_queue.get_all()
        pending = approval_queue.get_pending()

        return {
            "total": len(all_items),
            "pending": len(pending),
            "approved": sum(
                1 for item in all_items
                if item["status"] == "APPROVED"
            ),
            "rejected": sum(
                1 for item in all_items
                if item["status"] == "REJECTED"
            ),
            "completed": sum(
                1 for item in all_items
                if item["status"] == "COMPLETED"
            ),
            "failed": sum(
                1 for item in all_items
                if item["status"] == "FAILED"
            )
        }


approval_control = ApprovalControl()


def get_pending_approvals():
    return approval_control.pending()


def get_approval(approval_id):
    return approval_control.get(
        approval_id
    )


def approve(approval_id):
    return approval_control.approve(
        approval_id
    )


def reject(approval_id):
    return approval_control.reject(
        approval_id
    )


def complete(approval_id, result=None):
    return approval_control.complete(
        approval_id,
        result
    )


def fail(approval_id, error=None):
    return approval_control.fail(
        approval_id,
        error
    )


def approval_summary():
    return approval_control.summary()
