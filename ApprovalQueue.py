import datetime
import uuid


class ApprovalQueue:
    def __init__(self):
        self._queue = {}

    def add(
        self,
        action,
        agent=None,
        platform=None,
        file_path=None,
        title=None,
        description=None
    ):
        approval_id = str(uuid.uuid4())

        item = {
            "approval_id": approval_id,
            "action": action,
            "agent": agent,
            "platform": platform,
            "file_path": file_path,
            "title": title or action,
            "description": description or "",
            "status": "PENDING",
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat()
        }

        self._queue[approval_id] = item
        return item

    def get(self, approval_id):
        return self._queue.get(approval_id)

    def get_pending(self):
        return [
            item
            for item in self._queue.values()
            if item["status"] == "PENDING"
        ]

    def get_all(self):
        return list(self._queue.values())

    def approve(self, approval_id):
        item = self.get(approval_id)

        if not item:
            return None

        item["status"] = "APPROVED"
        item["updated_at"] = datetime.datetime.now().isoformat()

        return item

    def reject(self, approval_id):
        item = self.get(approval_id)

        if not item:
            return None

        item["status"] = "REJECTED"
        item["updated_at"] = datetime.datetime.now().isoformat()

        return item

    def complete(self, approval_id, result=None):
        item = self.get(approval_id)

        if not item:
            return None

        item["status"] = "COMPLETED"
        item["result"] = result
        item["updated_at"] = datetime.datetime.now().isoformat()

        return item

    def fail(self, approval_id, error=None):
        item = self.get(approval_id)

        if not item:
            return None

        item["status"] = "FAILED"
        item["error"] = str(error) if error else None
        item["updated_at"] = datetime.datetime.now().isoformat()

        return item

    def remove(self, approval_id):
        return self._queue.pop(
            approval_id,
            None
        )

    def clear_completed(self):
        completed = [
            approval_id
            for approval_id, item in self._queue.items()
            if item["status"] in {
                "COMPLETED",
                "REJECTED"
            }
        ]

        for approval_id in completed:
            del self._queue[approval_id]

        return len(completed)


approval_queue = ApprovalQueue()


def add_approval(
    action,
    agent=None,
    platform=None,
    file_path=None,
    title=None,
    description=None
):
    return approval_queue.add(
        action,
        agent,
        platform,
        file_path,
        title,
        description
    )


def get_approval(approval_id):
    return approval_queue.get(approval_id)


def get_pending_approvals():
    return approval_queue.get_pending()


def get_all_approvals():
    return approval_queue.get_all()


def approve_approval(approval_id):
    return approval_queue.approve(approval_id)


def reject_approval(approval_id):
    return approval_queue.reject(approval_id)


def complete_approval(approval_id, result=None):
    return approval_queue.complete(
        approval_id,
        result
    )


def fail_approval(approval_id, error=None):
    return approval_queue.fail(
        approval_id,
        error
    )
