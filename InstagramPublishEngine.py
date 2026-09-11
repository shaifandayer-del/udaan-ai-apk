
import os
import requests


class InstagramPublishEngine:

    def __init__(self):

        self.graph_url = "https://graph.facebook.com/v23.0"

        self.access_token = os.environ.get(
            "INSTAGRAM_ACCESS_TOKEN",
            ""
        )

        self.instagram_account_id = os.environ.get(
            "INSTAGRAM_ACCOUNT_ID",
            ""
        )

    def publish_video(
        self,
        video_url,
        caption=""
    ):

        if not self.access_token:
            return {
                "status": "FAILED",
                "message": "Instagram access token not configured."
            }

        if not self.instagram_account_id:
            return {
                "status": "FAILED",
                "message": "Instagram account ID not configured."
            }

        if not video_url:
            return {
                "status": "FAILED",
                "message": "Public video URL required."
            }

        try:

            create_url = (
                f"{self.graph_url}/"
                f"{self.instagram_account_id}/media"
            )

            create_response = requests.post(
                create_url,
                data={
                    "media_type": "REELS",
                    "video_url": video_url,
                    "caption": caption,
                    "access_token": self.access_token
                },
                timeout=60
            )

            create_data = create_response.json()

            if create_response.status_code >= 400:
                return {
                    "status": "FAILED",
                    "message": "Instagram media creation failed.",
                    "error": create_data
                }

            creation_id = create_data.get(
                "id"
            )

            if not creation_id:
                return {
                    "status": "FAILED",
                    "message": "Instagram creation ID missing."
                }

            publish_url = (
                f"{self.graph_url}/"
                f"{self.instagram_account_id}/media_publish"
            )

            publish_response = requests.post(
                publish_url,
                data={
                    "creation_id": creation_id,
                    "access_token": self.access_token
                },
                timeout=60
            )

            publish_data = publish_response.json()

            if publish_response.status_code >= 400:
                return {
                    "status": "FAILED",
                    "message": "Instagram publishing failed.",
                    "error": publish_data
                }

            return {
                "status": "SUCCESS",
                "platform": "Instagram",
                "media_id": publish_data.get("id"),
                "message": "Instagram video published successfully."
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "message": "Instagram API error.",
                "error": str(error)
            }


_engine = InstagramPublishEngine()


def publish_instagram_video(
    video_url,
    caption=""
):

    return _engine.publish_video(
        video_url,
        caption
    )
