import importlib
from pathlib import Path


def _load(name):
    try:
        return importlib.import_module(name)
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def _call(module, functions, video_path, title="", description="", caption=""):
    for name in functions:
        function = getattr(module, name, None)

        if not callable(function):
            continue

        calls = [
            lambda: function(
                video_path=video_path,
                title=title,
                description=description,
                caption=caption
            ),
            lambda: function(
                video_path,
                title,
                description
            ),
            lambda: function(video_path),
            lambda: function()
        ]

        for call in calls:
            try:
                result = call()

                if isinstance(result, dict):
                    return result

                return {
                    "status": "SUCCESS",
                    "result": result
                }

            except TypeError:
                continue
            except Exception as error:
                return {
                    "status": "FAILED",
                    "error": f"{type(error).__name__}: {error}"
                }

    return {
        "status": "FAILED",
        "message": "Upload function nahi mila."
    }


def upload_to_youtube(
    video_path="",
    title="UDAAN AI Video",
    description=""
):
    module, error = _load("YouTubeUploader")

    if module is None:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "message": "YouTubeUploader module load nahi hua.",
            "error": error
        }

    return _call(
        module,
        [
            "upload_video",
            "upload_to_youtube",
            "publish_video",
            "upload"
        ],
        video_path,
        title,
        description
    )


def publish_to_instagram(
    video_path="",
    caption=""
):
    module, error = _load("InstagramPublishEngine")

    if module is None:
        return {
            "status": "FAILED",
            "platform": "Instagram",
            "message": "InstagramPublishEngine module load nahi hua.",
            "error": error
        }

    return _call(
        module,
        [
            "publish_video",
            "publish_reel",
            "upload_video",
            "publish"
        ],
        video_path,
        caption=caption
    )


def execute_approved_upload(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption="",
    youtube=True,
    instagram=True
):
    path = Path(video_path)

    if not path.exists():
        return {
            "status": "FAILED",
            "message": "Approved video file nahi mili.",
            "video_path": str(path)
        }

    results = {}

    if youtube:
        results["youtube"] = upload_to_youtube(
            video_path=str(path),
            title=title,
            description=description
        )

    if instagram:
        results["instagram"] = publish_to_instagram(
            video_path=str(path),
            caption=caption
        )

    successful = [
        result
        for result in results.values()
        if result.get("status") == "SUCCESS"
    ]

    failed = [
        result
        for result in results.values()
        if result.get("status") != "SUCCESS"
    ]

    if successful and not failed:
        status = "SUCCESS"
    elif successful and failed:
        status = "PARTIAL_SUCCESS"
    else:
        status = "FAILED"

    return {
        "status": status,
        "video_path": str(path),
        "title": title,
        "youtube": results.get("youtube"),
        "instagram": results.get("instagram"),
        "results": results,
        "message": "Approved upload workflow completed."
    }


def run(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption=""
):
    return execute_approved_upload(
        video_path=video_path,
        title=title,
        description=description,
        caption=caption
    )


def execute(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption=""
):
    return run(video_path, title, description, caption)


def process(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption=""
):
    return run(video_path, title, description, caption)


def handle(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption=""
):
    return run(video_path, title, description, caption)


def run_agent(
    video_path="",
    title="UDAAN AI Video",
    description="",
    caption=""
):
    return run(video_path, title, description, caption)
