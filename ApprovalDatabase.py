import json
import os
from datetime import datetime


APPROVAL_FILE = "approvals.json"


def _load_approvals():
    if not os.path.exists(APPROVAL_FILE):
        return []

    try:
        with open(
            APPROVAL_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except Exception:
        return []


def _save_approvals(approvals):
    with open(
        APPROVAL_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            approvals,
            file,
            indent=2,
            ensure_ascii=False,
            default=str
        )


def save_approval(approval):
    approvals = _load_approvals()

    if not isinstance(approval, dict):
        return None

    approval = dict(approval)

    approval.setdefault(
        "created_at",
        datetime.utcnow().isoformat()
    )

    approvals.append(approval)
    _save_approvals(approvals)

    return approval


def get_approval_from_db(approval_id):
    approvals = _load_approvals()

    for approval in approvals:
        if str(approval.get("id")) == str(approval_id):
            return approval

    return None


def get_all_approvals():
    return _load_approvals()


def get_pending_approvals_from_db():
    approvals = _load_approvals()

    return [
        approval
        for approval in approvals
        if str(
            approval.get("status", "PENDING")
        ).upper() == "PENDING"
    ]


def update_approval(approval_id, status):
    approvals = _load_approvals()

    updated = None

    for approval in approvals:
        if str(approval.get("id")) == str(approval_id):
            approval["status"] = status
            approval["updated_at"] = datetime.utcnow().isoformat()
            updated = approval
            break

    if updated is not None:
        _save_approvals(approvals)

    return updated


def delete_approval(approval_id):
    approvals = _load_approvals()

    remaining = [
        approval
        for approval in approvals
        if str(approval.get("id")) != str(approval_id)
    ]

    if len(remaining) == len(approvals):
        return False

    _save_approvals(remaining)
    return True
