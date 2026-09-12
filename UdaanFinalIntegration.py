import importlib


def _load_module(name):
    try:
        return importlib.import_module(name)
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def _run(module_name, function_names, **kwargs):
    module, error = _load_module(module_name)

    if module is None:
        return {
            "status": "FAILED",
            "module": module_name,
            "error": error
        }

    for function_name in function_names:
        function = getattr(module, function_name, None)

        if not callable(function):
            continue

        try:
            return function(**kwargs)
        except TypeError:
            try:
                return function(kwargs.get("command", ""))
            except Exception as inner_error:
                return {
                    "status": "FAILED",
                    "module": module_name,
                    "error": f"{type(inner_error).__name__}: {inner_error}"
                }
        except Exception as error:
            return {
                "status": "FAILED",
                "module": module_name,
                "error": f"{type(error).__name__}: {error}"
            }

    return {
        "status": "FAILED",
        "module": module_name,
        "message": "Required function nahi mila."
    }


def create_video(command=""):
    return _run(
        "VideoProductionPipeline",
        [
            "create_video_project",
            "generate_video",
            "create_video",
            "run"
        ],
        command=command
    )


def submit_for_approval(
    video_path="",
    title="UDAAN AI Video",
    description=""
):
    return _run(
        "VideoApprovalController",
        [
            "request_approval",
            "create_approval",
            "submit_for_approval",
            "submit"
        ],
        video_path=video_path,
        title=title,
        description=description
    )


def execute_approved(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption=""
):
    return _run(
        "ApprovedUploadRunner",
        [
            "execute_approved_upload",
            "run",
            "execute"
        ],
        video_path=video_path,
        title=title,
        description=description,
        caption=caption
    )


def run_full_workflow(
    command="",
    auto_approval=False
):
    if not command or not command.strip():
        return {
            "status": "FAILED",
            "message": "Founder command empty hai."
        }

    video = create_video(command)

    if video.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "VIDEO_CREATION",
            "video": video
        }

    video_path = (
        video.get("video_path")
        or video.get("output_path")
        or video.get("render", {}).get("video_path", "")
    )

    title = video.get(
        "title",
        "UDAAN AI Video"
    )

    description = video.get(
        "description",
        ""
    )

    approval = submit_for_approval(
        video_path=video_path,
        title=title,
        description=description
    )

    if approval.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "APPROVAL",
            "video": video,
            "approval": approval
        }

    if not auto_approval:
        return {
            "status": "SUCCESS",
            "stage": "WAITING_FOR_APPROVAL",
            "video": video,
            "approval": approval,
            "approval_required": True,
            "publish_status": "WAITING_FOR_FOUNDER_APPROVAL"
        }

    upload = execute_approved(
        video_path=video_path,
        title=title,
        description=description
    )

    return {
        "status": upload.get("status", "FAILED"),
        "stage": "PUBLISH",
        "video": video,
        "approval": approval,
        "upload": upload
    }


def run(command=""):
    return run_full_workflow(command)


def execute(command=""):
    return run_full_workflow(command)


def process(command=""):
    return run_full_workflow(command)


def handle(command=""):
    return run_full_workflow(command)


def run_agent(command=""):
    return run_full_workflow(command)
