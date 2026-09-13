import json
import os
import threading
from datetime import datetime, timezone


APPROVAL_DATABASE_FILE = os.getenv(
    "UDAAN_APPROVAL_DATABASE",
    "approvals.json"
)

_lock = threading.Lock()


def _now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def _load():
    with _lock:
        if not os.path.exists(
            APPROVAL_DATABASE_FILE
        ):
            return []

        try:
            with open(
                APPROVAL_DATABASE_FILE,
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
    with _lock:
        temp_file = (
            APPROVAL_DATABASE_FILE
            + ".tmp"
        )

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
            APPROVAL_DATABASE_FILE
        )

    return True


def create_approval(
    action,
    platform=None,
    file_path=None,
    title=None,
    description=None,
    agent=None,
    command=None,
    metadata=None
):
    data = _load()

    approval_id = (
        f"approval_"
        f"{int(datetime.now().timestamp() * 1000)}"
    )

    item = {
        "approval_id": approval_id,
        "id": approval_id,
        "action": action,
        "platform": platform,
        "file_path": file_path,
        "title": title or "UDAAN AI Approval",
        "description": description or "",
        "agent": agent,
        "command": command,
        "metadata": metadata or {},
        "status": "PENDING",
        "created_at": _now(),
        "updated_at": _now(),
        "executed": False
    }

    data.append(item)
    _save(data)

    return item


def save_approval(approval):
    if not isinstance(approval, dict):
        return None

    approval_id = (
        approval.get("approval_id")
        or approval.get("id")
    )

    if not approval_id:
        approval_id = (
            f"approval_"
            f"{int(datetime.now().timestamp() * 1000)}"
        )

    approval["approval_id"] = approval_id
    approval["id"] = approval_id
    approval.setdefault(
        "status",
        "PENDING"
    )
    approval.setdefault(
        "created_at",
        _now()
    )
    approval["updated_at"] = _now()
    approval.setdefault(
        "executed",
        False
    )

    data = _load()

    found = False

    for index, item in enumerate(data):
        if (
            item.get("approval_id")
            == approval_id
            or item.get("id")
            == approval_id
        ):
            data[index] = approval
            found = True
            break

    if not found:
        data.append(approval)

    _save(data)

    return approval


def get_approval_from_db(
    approval_id
):
    data = _load()

    for item in data:
        if (
            item.get("approval_id")
            == approval_id
            or item.get("id")
            == approval_id
        ):
            return item

    return None


def get_approval(
    approval_id
):
    return get_approval_from_db(
        approval_id
    )


def get_all_approvals():
    return _load()


def get_pending_approvals():
    data = _load()

    return [
        item
        for item in data
        if str(
            item.get(
                "status",
                ""
            )
        ).upper()
        == "PENDING"
    ]


def get_pending_approvals_from_db():
    return get_pending_approvals()


def get_pending_approvals_db():
    return get_pending_approvals()


def update_approval(
    approval_id,
    status=None,
    **updates
):
    data = _load()

    for item in data:
        if (
            item.get("approval_id")
            == approval_id
            or item.get("id")
            == approval_id
        ):
            if status is not None:
                item["status"] = status

            for key, value in updates.items():
                item[key] = value

            item["updated_at"] = _now()

            _save(data)

            return item

    return None


def update_approval_status(
    approval_id,
    status
):
    return update_approval(
        approval_id,
        status
    )


def approve_approval(
    approval_id,
    result=None
):
    return update_approval(
        approval_id,
        "APPROVED",
        result=result,
        executed=False
    )


def reject_approval(
    approval_id,
    reason=None
):
    return update_approval(
        approval_id,
        "REJECTED",
        rejection_reason=reason,
        executed=False
    )


def mark_executed(
    approval_id,
    result=None
):
    return update_approval(
        approval_id,
        "EXECUTED",
        result=result,
        executed=True,
        executed_at=_now()
    )


def get_approval_status(
    approval_id
):
    approval = get_approval(
        approval_id
    )

    if not approval:
        return None

    return approval.get(
        "status",
        "UNKNOWN"
    )


def approval_exists(
    approval_id
):
    return (
        get_approval(
            approval_id
        )
        is not None
    )


def delete_approval(
    approval_id
):
    data = _load()

    new_data = [
        item
        for item in data
        if (
            item.get("approval_id")
            != approval_id
            and item.get("id")
            != approval_id
        )
    ]

    changed = len(new_data) != len(data)

    if changed:
        _save(new_data)

    return changed


def clear_completed_approvals():
    data = _load()

    new_data = [
        item
        for item in data
        if str(
            item.get(
                "status",
                ""
            )
        ).upper()
        not in [
            "EXECUTED",
            "COMPLETED"
        ]
    ]

    _save(new_data)

    return True


def count_pending_approvals():
    return len(
        get_pending_approvals()
    )


def get_database_status():
    try:
        data = _load()

        return {
            "status": "READY",
            "database": APPROVAL_DATABASE_FILE,
            "total_approvals": len(data),
            "pending": len(
                [
                    item
                    for item in data
                    if str(
                        item.get(
                            "status",
                            ""
                        )
                    ).upper()
                    == "PENDING"
                ]
            )
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "database": APPROVAL_DATABASE_FILE,
            "error": str(error)
        }


def initialize_approval_database():
    if not os.path.exists(
        APPROVAL_DATABASE_FILE
    ):
        _save([])

    return True


initialize_approval_database()
