import os
import requests


GRAPH_API_VERSION = "v23.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def _get_token():
    return (
        os.getenv("INSTAGRAM_ACCESS_TOKEN")
        or os.getenv("META_ACCESS_TOKEN")
        or ""
    )


def _get_ig_user_id():
    return (
        os.getenv("INSTAGRAM_USER_ID")
        or os.getenv("IG_USER_ID")
        or ""
    )


def _request(method, url, **kwargs):
    try:
        response = requests.request(
            method,
            url,
            timeout=60,
            **kwargs
        )

        try:
            data = response.json()
        except ValueError:
            data = {
                "raw": response.text
            }

        if response.ok:
            return {
                "status": "SUCCESS",
                "data": data
            }

        return {
            "status": "FAILED",
            "message": "Instagram API request failed.",
            "error": data
        }

    except requests.RequestException as error:
        return {
            "status": "FAILED",
            "message": "Instagram connection failed.",
            "error": f"{type(error).__name__}: {error}"
        }


def check_connection():
    token = _get_token()
    user_id = _get_ig_user_id()

    if not token:
        return {
            "status": "FAILED",
            "message": "INSTAGRAM_ACCESS_TOKEN configured nahi hai."
        }

    if not user_id:
        return {
            "status": "FAILED",
            "message": "INSTAGRAM_USER_ID configured nahi hai."
        }

    result = _request(
        "GET",
        f"{GRAPH_API_BASE}/{user_id}",
        params={
            "fields": "id,username",
            "access_token": token
        }
    )

    if result["status"] != "SUCCESS":
        return result

    data = result.get("data", {})

    return {
        "status": "SUCCESS",
        "platform": "Instagram",
        "connected": True,
        "user_id": data.get("id", user_id),
        "username": data.get("username", "")
    }


def create_media_container(
    video_url="",
    caption=""
):
    token = _get_token()
    user_id = _get_ig_user_id()

    if not token:
        return {
            "status": "FAILED",
            "message": "Instagram access token missing."
        }

    if not user_id:
        return {
            "status": "FAILED",
            "message": "Instagram user ID missing."
        }

    if not video_url:
        return {
            "status": "FAILED",
            "message": "Public video URL required."
        }

    return _request(
        "POST",
        f"{GRAPH_API_BASE}/{user_id}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": token
        }
    )


def publish_container(container_id):
    token = _get_token()
    user_id = _get_ig_user_id()

    if not token or not user_id:
        return {
            "status": "FAILED",
            "message": "Instagram credentials missing."
        }

    if not container_id:
        return {
            "status": "FAILED",
            "message": "Instagram media container ID missing."
        }

    return _request(
        "POST",
        f"{GRAPH_API_BASE}/{user_id}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": token
        }
    )


def publish_video(
    video_url="",
    caption=""
):
    container = create_media_container(
        video_url=video_url,
        caption=caption
    )

    if container.get("status") != "SUCCESS":
        return container

    container_data = container.get("data", {})
    container_id = container_data.get("id")

    if not container_id:
        return {
            "status": "FAILED",
            "message": "Instagram container ID nahi mila.",
            "container": container
        }

    publish = publish_container(container_id)

    if publish.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "PUBLISH",
            "container": container,
            "publish": publish
        }

    publish_data = publish.get("data", {})

    return {
        "status": "SUCCESS",
        "platform": "Instagram",
        "container_id": container_id,
        "media_id": publish_data.get("id"),
        "message": "Instagram video successfully published."
    }


def run(command=""):
    return {
        "status": "SUCCESS",
        "agent": "Instagram",
        "command": command,
        "message": "Instagram publishing engine ready.",
        "connected": check_connection()
    }


def execute(command=""):
    return run(command)


def process(command=""):
    return run(command)


def handle(command=""):
    return run(command)


def run_agent(command=""):
    return run(command)
