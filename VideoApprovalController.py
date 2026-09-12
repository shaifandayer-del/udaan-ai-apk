import importlib


def _load(name):
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def _result(status, message, **extra):
    return {
        "status": status,
        "message": message,
        **extra
    }


def create_video_preview(
    video_path="",
    title="UDAAN AI Video",
    platform="YouTube",
    description=""
):
    preview = _load("VideoPreview")

    if preview is None:
        return _result(
            "FAILED",
            "VideoPreview module load nahi hua."
        )

    function = getattr(preview, "create_preview", None)

    if not callable(function):
        return _result(
            "FAILED",
            "VideoPreview function nahi mila."
        )

    try:
        result = function(
            video_path=video_path,
            title=title,
            platform=platform,
            description=description
        )

        if isinstance(result, dict):
            result.setdefault("status", "SUCCESS")
            result.setdefault("approval_required", True)
            return result

        return _result(
            "SUCCESS",
            "Video preview created.",
            preview=result,
            approval_required=True
        )

    except Exception as error:
        return _result(
            "FAILED",
            "Video preview create failed.",
            error=f"{type(error).__name__}: {error}"
        )


def create_video_for_approval(
    video_path="",
    title="UDAAN AI Video",
    platform="YouTube",
    description=""
):
    return create_video_preview(
        video_path,
        title,
        platform,
        description
    )


def get_video_preview(approval_id):
    approval = _load("FounderApproval")

    if approval is None:
        return _result(
            "FAILED",
            "FounderApproval module load nahi hua."
        )

    function = getattr(approval, "get_approval", None)

    if not callable(function):
        return _result(
            "FAILED",
            "get_approval function nahi mila."
        )

    try:
        result = function(approval_id)

        if not result:
            return _result(
                "FAILED",
                "Approval request not found."
            )

        return {
            "status": "SUCCESS",
            "approval": result
        }

    except Exception as error:
        return _result(
            "FAILED",
            "Approval preview fetch failed.",
            error=f"{type(error).__name__}: {error}"
        )


def get_request(approval_id):
    return get_video_preview(approval_id)


def approve_video(approval_id):
    approval = _load("FounderApproval")

    if approval is None:
        return _result(
            "FAILED",
            "FounderApproval module load nahi hua."
        )

    get_function = getattr(approval, "get_approval", None)
    approve_function = getattr(approval, "approve", None)

    if not callable(get_function) or not callable(approve_function):
        return _result(
            "FAILED",
            "Approval functions nahi mile."
        )

    try:
        request = get_function(approval_id)

        if not request:
            return _result(
                "FAILED",
                "Approval request not found."
            )

        if request.get("status") != "PENDING":
            return _result(
                "FAILED",
                "Approval already processed.",
                approval=request
            )

        result = approve_function(approval_id)

        if isinstance(result, dict):
            return result

        return _result(
            "SUCCESS",
            "Video approved.",
            approval_id=approval_id,
            result=result
        )

    except Exception as error:
        return _result(
            "FAILED",
            "Video approval failed.",
            error=f"{type(error).__name__}: {error}"
        )


def reject_video(approval_id):
    approval = _load("FounderApproval")

    if approval is None:
        return _result(
            "FAILED",
            "FounderApproval module load nahi hua."
        )

    get_function = getattr(approval, "get_approval", None)
    reject_function = getattr(approval, "reject", None)

    if not callable(get_function) or not callable(reject_function):
        return _result(
            "FAILED",
            "Approval functions nahi mile."
        )

    try:
        request = get_function(approval_id)

        if not request:
            return _result(
                "FAILED",
                "Approval request not found."
            )

        if request.get("status") != "PENDING":
            return _result(
                "FAILED",
                "Approval already processed.",
                approval=request
            )

        result = reject_function(approval_id)

        if isinstance(result, dict):
            return result

        return _result(
            "SUCCESS",
            "Video rejected.",
            approval_id=approval_id,
            result=result
        )

    except Exception as error:
        return _result(
            "FAILED",
            "Video rejection failed.",
            error=f"{type(error).__name__}: {error}"
        )


def run(command=""):
    return {
        "status": "SUCCESS",
        "agent": "Video Approval Controller",
        "message": "Video approval controller ready."
    }


def execute(command=""):
    return run(command)


def process(command=""):
    return run(command)


def handle(command=""):
    return run(command)


def run_agent(command=""):
    return run(command)
