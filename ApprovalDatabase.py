import json
import os
import uuid
from datetime import datetime, timezone


APPROVAL_FILE = "approvals.json"


def _now():
    return datetime.now(timezone.utc).isoformat()


def _load():
    if not os.path.exists(APPROVAL_FILE):
        return []

    try:
        with open(
            APPROVAL_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def _save(data):
    temp_file = APPROVAL_FILE + ".tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    os.replace(
        temp_file,
        APPROVAL_FILE
    )


def create_approval(
    action,
    agent=None,
    platform=None,
    file_path=None,
    title=None,
    description=None,
    metadata=None
):
    approvals = _load()

    approval = {
        "id": str(uuid.uuid4()),
        "action": str(action or ""),
        "agent": agent,
        "platform": platform,
        "file_path": file_path,
        "title": title or str(action or "UDAAN AI Approval"),
        "description": description or "",
        "metadata": metadata or {},
        "status": "PENDING",
        "created_at": _now(),
        "updated_at": _now(),
        "approved_at": None,
        "rejected_at": None
    }

    approvals.append(approval)
    _save(approvals)

    return approval


def save_approval(approval):
    approvals = _load()

    if not isinstance(approval, dict):
        return None

    item = dict(approval)

    item.setdefault(
        "id",
        str(uuid.uuid4())
    )

    item.setdefault(
        "status",
        "PENDING"
    )

    item.setdefault(
        "created_at",
        _now()
    )

    item["updated_at"] = _now()

    existing = False

    for index, current in enumerate(approvals):
        if str(current.get("id")) == str(item["id"]):
            approvals[index] = item
            existing = True
            break

    if not existing:
        approvals.append(item)

    _save(approvals)

    return item


def get_approval_from_db(approval_id):
    approvals = _load()

    for approval in approvals:
        if str(approval.get("id")) == str(approval_id):
            return approval

    return None


def get_approval(approval_id):
    return get_approval_from_db(
        approval_id
    )


def get_all_approvals():
    return _load()


def get_pending_approvals():
    approvals = _load()

    return [
        approval
        for approval in approvals
        if str(
            approval.get(
                "status",
                "PENDING"
            )
        ).upper() == "PENDING"
    ]


def get_pending_approvals_from_db():
    return get_pending_approvals()


def approve_approval(approval_id):
    return update_approval(
        approval_id,
        "APPROVED"
    )


def reject_approval(approval_id):
    return update_approval(
        approval_id,
        "REJECTED"
    )


def update_approval(
    approval_id,
    status
):
    approvals = _load()
    updated = None

    normalized_status = str(
        status or ""
    ).upper()

    for approval in approvals:
        if str(
            approval.get("id")
        ) == str(approval_id):

            approval["status"] = normalized_status
            approval["updated_at"] = _now()

            if normalized_status == "APPROVED":
                approval["approved_at"] = _now()

            elif normalized_status == "REJECTED":
                approval["rejected_at"] = _now()

            updated = approval
            break

    if updated is not None:
        _save(approvals)

    return updated


def delete_approval(approval_id):
    approvals = _load()

    remaining = [
        approval
        for approval in approvals
        if str(
            approval.get("id")
        ) != str(approval_id)
    ]

    if len(remaining) == len(approvals):
        return False

    _save(remaining)

    return True


def clear_completed_approvals():
    approvals = _load()

    active = [
        approval
        for approval in approvals
        if str(
            approval.get(
                "status",
                "PENDING"
            )
        ).upper()
        not in {
            "APPROVED",
            "REJECTED",
            "EXECUTED"
        }
    ]

    _save(active)

    return active


def mark_executed(approval_id):
    return update_approval(
        approval_id,
        "EXECUTED"
    )


def get_approval_status(approval_id):
    approval = get_approval_from_db(
        approval_id
    )

    if approval is None:
        return None

    return approval.get(
        "status",
        "UNKNOWN"
    )


def approval_exists(approval_id):
    return (
        get_approval_from_db(
            approval_id
        )
        is not None
    )


def count_pending_approvals():
    return len(
        get_pending_approvals()
    )


def get_database_status():
    approvals = _load()

    return {
        "status": "READY",
        "storage": APPROVAL_FILE,
        "total": len(approvals),
        "pending": len(
            [
                item
                for item in approvals
                if str(
                    item.get(
                        "status",
                        "PENDING"
                    )
                ).upper() == "PENDING"
            ]
        )
    }


def initialize_approval_database():
    if not os.path.exists(
        APPROVAL_FILE
    ):
        _save([])

    return get_database_status()


initialize_approval_database()
