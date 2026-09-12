import os
import importlib


PLATFORMS = {
    "youtube": "YouTubeOAuth",
    "instagram": "InstagramPublishEngine",
}


def _load_module(name):
    try:
        return importlib.import_module(name)
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def _youtube_status():
    module, error = _load_module("YouTubeOAuth")

    if module is None:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "connected": False,
            "error": error
        }

    function = getattr(module, "check_connection", None)

    if not callable(function):
        return {
            "status": "NOT_CONFIGURED",
            "platform": "YouTube",
            "connected": False
        }

    try:
        return function()
    except Exception as error:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "connected": False,
            "error": f"{type(error).__name__}: {error}"
        }


def _instagram_status():
    module, error = _load_module("InstagramPublishEngine")

    if module is None:
        return {
            "status": "FAILED",
            "platform": "Instagram",
            "connected": False,
            "error": error
        }

    function = getattr(module, "check_connection", None)

    if not callable(function):
        return {
            "status": "NOT_CONFIGURED",
            "platform": "Instagram",
            "connected": False
        }

    try:
        return function()
    except Exception as error:
        return {
            "status": "FAILED",
            "platform": "Instagram",
            "connected": False,
            "error": f"{type(error).__name__}: {error}"
        }


def check_platform(platform):
    name = str(platform).lower().strip()

    if name == "youtube":
        return _youtube_status()

    if name == "instagram":
        return _instagram_status()

    return {
        "status": "FAILED",
        "platform": platform,
        "connected": False,
        "message": "Platform supported nahi hai."
    }


def check_all():
    youtube = _youtube_status()
    instagram = _instagram_status()

    connected = (
        youtube.get("connected") is True
        and instagram.get("connected") is True
    )

    return {
        "status": "SUCCESS",
        "connected": connected,
        "youtube": youtube,
        "instagram": instagram
    }


def connect_youtube():
    module, error = _load_module("YouTubeOAuth")

    if module is None:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "error": error
        }

    function = getattr(module, "authenticate", None)

    if not callable(function):
        return {
            "status": "NOT_CONFIGURED",
            "platform": "YouTube",
            "message": "YouTube authentication function nahi mila."
        }

    try:
        return function()
    except Exception as error:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "error": f"{type(error).__name__}: {error}"
        }


def connect_instagram():
    token = (
        os.getenv("INSTAGRAM_ACCESS_TOKEN")
        or os.getenv("META_ACCESS_TOKEN")
        or ""
    )

    user_id = (
        os.getenv("INSTAGRAM_USER_ID")
        or os.getenv("IG_USER_ID")
        or ""
    )

    if not token:
        return {
            "status": "NOT_CONFIGURED",
            "platform": "Instagram",
            "connected": False,
            "message": "Instagram access token configured nahi hai."
        }

    if not user_id:
        return {
            "status": "NOT_CONFIGURED",
            "platform": "Instagram",
            "connected": False,
            "message": "Instagram user ID configured nahi hai."
        }

    return _instagram_status()


def connection_summary():
    result = check_all()

    return {
        "status": result.get("status"),
        "connected": result.get("connected"),
        "platforms": {
            "YouTube": result.get("youtube"),
            "Instagram": result.get("instagram")
        }
    }


def run(command=""):
    return {
        "status": "SUCCESS",
        "agent": "Multi Channel Auth Manager",
        "command": command,
        "connections": connection_summary()
    }


def execute(command=""):
    return run(command)


def process(command=""):
    return run(command)


def handle(command=""):
    return run(command)


def run_agent(command=""):
    return run(command)
