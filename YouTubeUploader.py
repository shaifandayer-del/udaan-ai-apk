import os
import json
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def _credentials():
    token_json = os.getenv("YOUTUBE_TOKEN_JSON", "")
    client_json = os.getenv("YOUTUBE_CLIENT_JSON", "")

    if token_json:
        try:
            info = json.loads(token_json)
            return Credentials.from_authorized_user_info(
                info,
                SCOPES
            )
        except Exception:
            pass

    if not client_json:
        return None

    try:
        client_config = json.loads(client_json)

        flow = InstalledAppFlow.from_client_config(
            client_config,
            SCOPES
        )

        return flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent"
        )

    except Exception:
        return None


def check_connection():
    credentials = _credentials()

    if credentials is None:
        return {
            "status": "NOT_CONFIGURED",
            "platform": "YouTube",
            "connected": False,
            "message": "YouTube OAuth credentials configured nahi hain."
        }

    try:
        youtube = build(
            "youtube",
            "v3",
            credentials=credentials
        )

        response = youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()

        items = response.get("items", [])

        if not items:
            return {
                "status": "FAILED",
                "platform": "YouTube",
                "connected": False,
                "message": "YouTube channel nahi mila."
            }

        channel = items[0]

        return {
            "status": "SUCCESS",
            "platform": "YouTube",
            "connected": True,
            "channel_id": channel.get("id"),
            "channel_name": channel.get("snippet", {}).get("title", "")
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "connected": False,
            "message": "YouTube connection failed.",
            "error": f"{type(error).__name__}: {error}"
        }


def upload_video(
    video_path="",
    title="UDAAN AI Video",
    description="",
    tags=None,
    privacy_status="private",
    category_id="22"
):
    if not video_path:
        return {
            "status": "FAILED",
            "message": "Video path required hai."
        }

    path = Path(video_path)

    if not path.exists():
        return {
            "status": "FAILED",
            "message": "Video file nahi mili.",
            "video_path": str(path)
        }

    if not path.is_file():
        return {
            "status": "FAILED",
            "message": "Video path valid file nahi hai.",
            "video_path": str(path)
        }

    if path.stat().st_size == 0:
        return {
            "status": "FAILED",
            "message": "Video file empty hai.",
            "video_path": str(path)
        }

    credentials = _credentials()

    if credentials is None:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "message": "YouTube OAuth credentials configured nahi hain."
        }

    if credentials.expired and credentials.refresh_token:
        try:
            from google.auth.transport.requests import Request

            credentials.refresh(Request())

        except Exception as error:
            return {
                "status": "FAILED",
                "platform": "YouTube",
                "message": "YouTube OAuth refresh failed.",
                "error": f"{type(error).__name__}: {error}"
            }

    try:
        youtube = build(
            "youtube",
            "v3",
            credentials=credentials
        )

        if tags is None:
            tags = []

        body = {
            "snippet": {
                "title": str(title)[:100],
                "description": str(description),
                "tags": tags,
                "categoryId": str(category_id)
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(
            str(path),
            mimetype="video/mp4",
            resumable=True
        )

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None

        while response is None:
            _, response = request.next_chunk()

        video_id = response.get("id")

        if not video_id:
            return {
                "status": "FAILED",
                "platform": "YouTube",
                "message": "YouTube video ID nahi mila.",
                "response": response
            }

        return {
            "status": "SUCCESS",
            "platform": "YouTube",
            "video_id": video_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "title": title,
            "privacy_status": privacy_status,
            "message": "Video successfully uploaded to YouTube."
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "platform": "YouTube",
            "message": "YouTube video upload failed.",
            "error": f"{type(error).__name__}: {error}"
        }


def upload_to_youtube(
    video_path="",
    title="UDAAN AI Video",
    description="",
    tags=None,
    privacy_status="private",
    category_id="22"
):
    return upload_video(
        video_path=video_path,
        title=title,
        description=description,
        tags=tags,
        privacy_status=privacy_status,
        category_id=category_id
    )


def publish_video(
    video_path="",
    title="UDAAN AI Video",
    description="",
    tags=None,
    privacy_status="private",
    category_id="22"
):
    return upload_video(
        video_path=video_path,
        title=title,
        description=description,
        tags=tags,
        privacy_status=privacy_status,
        category_id=category_id
    )


def run(command=""):
    return {
        "status": "SUCCESS",
        "agent": "YouTube",
        "command": command,
        "platform": "YouTube",
        "message": "YouTube uploader ready.",
        "connection": check_connection()
    }


def execute(command=""):
    return run(command)


def process(command=""):
    return run(command)


def handle(command=""):
    return run(command)


def run_agent(command=""):
    return run(command)
