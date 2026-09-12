import importlib
import os
from pathlib import Path


def _load_uploader():
    try:
        return importlib.import_module("YouTubeUploader")
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def _find_function(module):
    for name in (
        "upload_video",
        "upload_to_youtube",
        "publish_video",
        "upload",
        "run",
        "execute",
    ):
        function = getattr(module, name, None)
        if callable(function):
            return function
    return None


def check_credentials():
    token = (
        os.getenv("YOUTUBE_ACCESS_TOKEN")
        or os.getenv("YOUTUBE_OAUTH_TOKEN")
        or ""
    )

    client_id = os.getenv("YOUTUBE_CLIENT_ID", "")

    return {
        "status": "SUCCESS" if token or client_id else "NOT_CONFIGURED",
        "platform": "YouTube",
        "oauth_configured": bool(token),
        "client_id_configured": bool(client_id),
    }


def publish_video(
    video_path="",
    title="UDAAN AI Video",
    description="",
    tags=None,
    privacy_status="private",
    category_id="22",
):
    if not video_path:
        return {
            "status": "FAILED",
            "message": "YouTube upload ke liye video path required hai."
        }

    path = Path(video_path)

    if not path.exists() or not path.is_file():
        return {
            "status": "FAILED",
            "message": "Video file nahi mili.",
            "video_path": str(path)
        }

    if path.stat().st_size == 0:
        return {
            "status": "FAILED",
            "message": "Video file empty hai.",
            "video_path": str(path)
        }

    module, error = _load_uploader()

    if module is None:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "message": "YouTubeUploader module load nahi hua.",
            "error": error
        }

    function = _find_function(module)

    if function is None:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "message": "YouTube upload function nahi mila."
        }

    if tags is None:
        tags = []

    calls = [
        lambda: function(
            video_path=str(path),
            title=title,
            description=description,
            tags=tags,
            privacy_status=privacy_status,
            category_id=category_id
        ),
        lambda: function(
            video_path=str(path),
            title=title,
            description=description
        ),
        lambda: function(
            str(path),
            title,
            description
        ),
        lambda: function(str(path)),
    ]

    for call in calls:
        try:
            result = call()

            if isinstance(result, dict):
                result.setdefault("platform", "YouTube")
                result.setdefault("video_path", str(path))
                return result

            return {
                "status": "SUCCESS",
                "platform": "YouTube",
                "video_path": str(path),
                "result": result,
                "message": "YouTube publish completed."
            }

        except TypeError:
            continue

        except Exception as error:
            return {
                "status": "FAILED",
                "platform": "YouTube",
                "video_path": str(path),
                "message": "YouTube publish failed.",
                "error": f"{type(error).__name__}: {error}"
            }

    return {
        "status": "FAILED",
        "platform": "YouTube",
        "video_path": str(path),
        "message": "YouTubeUploader compatible function nahi mila."
    }


def upload_video(
    video_path="",
    title="UDAAN AI Video",
    description="",
    tags=None,
    privacy_status="private",
    category_id="22",
):
    return publish_video(
        video_path=video_path,
        title=title,
        description=description,
        tags=tags,
        privacy_status=privacy_status,
        category_id=category_id,
    )


def run(command=""):
    return {
        "status": "SUCCESS",
        "agent": "YouTube",
        "command": command,
        "platform": "YouTube",
        "message": "YouTube publish engine ready.",
        "credentials": check_credentials(),
    }


def execute(command=""):
    return run(command)


def process(command=""):
    return run(command)


def handle(command=""):
    return run(command)


def run_agent(command=""):
    return run(command)
