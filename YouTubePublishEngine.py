File name: YouTubePublishEngine.py

# ==========================================
# UDAAN AI - YOUTUBE PUBLISH ENGINE
# STEP 123
# ==========================================

import os
import json
import pickle
from datetime import datetime

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    build = None
    MediaFileUpload = None


TOKEN_FILE = "youtube_token.pickle"


class YouTubePublishEngine:

    def __init__(self):
        self.scope = (
            "https://www.googleapis.com/auth/youtube.upload"
        )

    def timestamp(self):
        return datetime.now().isoformat()

    def check_dependencies(self):

        if build is None or MediaFileUpload is None:
            return {
                "status": "NOT_READY",
                "message":
                    "Google YouTube API packages missing."
            }

        return {
            "status": "READY"
        }

    def check_token(self):

        if not os.path.exists(TOKEN_FILE):
            return {
                "status": "NOT_AUTHENTICATED",
                "message":
                    "YouTube OAuth token not found."
            }

        return {
            "status": "AUTHENTICATED"
        }

    def publish(
        self,
        video_path,
        title,
        description="",
        tags=None,
        category_id="22",
        privacy_status="private"
    ):

        if not video_path:
            return {
                "status": "FAILED",
                "message": "Video file path missing."
            }

        if not os.path.exists(video_path):
            return {
                "status": "FILE_NOT_FOUND",
                "video_path": video_path
            }

        if not title:
            return {
                "status": "FAILED",
                "message": "Video title missing."
            }

        dependency_status = (
            self.check_dependencies()
        )

        if dependency_status["status"] != "READY":
            return dependency_status

        token_status = self.check_token()

        if token_status["status"] != "AUTHENTICATED":
            return token_status

        try:

            with open(
                TOKEN_FILE,
                "rb"
            ) as token_file:

                credentials = pickle.load(
                    token_file
                )

            youtube = build(
                "youtube",
                "v3",
                credentials=credentials
            )

            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus":
                        privacy_status
                }
            }

            if tags:
                body["snippet"]["tags"] = tags

            media = MediaFileUpload(
                video_path,
                mimetype="video/mp4",
                resumable=True
            )

            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = request.execute()

            video_id = response.get(
                "id"
            )

            return {
                "status": "SUCCESS",
                "platform": "YouTube",
                "video_id": video_id,
                "url":
                    "https://www.youtube.com/watch?v="
                    + str(video_id),
                "title": title,
                "privacy_status":
                    privacy_status,
                "published_at":
                    self.timestamp()
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "platform": "YouTube",
                "message":
                    "YouTube upload failed.",
                "error": str(error)
            }


_publisher = YouTubePublishEngine()


def publish_video(
    video_path,
    title,
    description="",
    tags=None,
    category_id="22",
    privacy_status="private"
):

    return _publisher.publish(
        video_path,
        title,
        description,
        tags,
        category_id,
        privacy_status
    )


def check_youtube_publisher():

    return {
        "dependencies":
            _publisher.check_dependencies(),
        "oauth":
            _publisher.check_token()
    }
