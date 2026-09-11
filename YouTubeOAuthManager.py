# ==========================================
# UDAAN AI - YOUTUBE OAUTH MANAGER
# STEP 132
# ==========================================

import os
import pickle


class YouTubeOAuthManager:

    def __init__(
        self,
        token_dir="youtube_tokens"
    ):
        self.token_dir = token_dir
        os.makedirs(self.token_dir, exist_ok=True)

    def token_path(self, channel_id):

        safe_id = str(channel_id).replace(
            "/", "_"
        ).replace(
            "\\", "_"
        )

        return os.path.join(
            self.token_dir,
            f"{safe_id}.pickle"
        )

    def save_token(
        self,
        channel_id,
        credentials
    ):

        path = self.token_path(channel_id)

        with open(path, "wb") as file:
            pickle.dump(
                credentials,
                file
            )

        return {
            "status": "SUCCESS",
            "channel_id": channel_id,
            "token_path": path
        }

    def load_token(self, channel_id):

        path = self.token_path(channel_id)

        if not os.path.exists(path):

            return {
                "status": "NOT_FOUND",
                "channel_id": channel_id
            }

        try:

            with open(path, "rb") as file:
                credentials = pickle.load(file)

            return {
                "status": "SUCCESS",
                "channel_id": channel_id,
                "credentials": credentials
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "channel_id": channel_id,
                "error": str(error)
            }

    def remove_token(self, channel_id):

        path = self.token_path(channel_id)

        if os.path.exists(path):
            os.remove(path)

        return {
            "status": "SUCCESS",
            "channel_id": channel_id
        }


_manager = YouTubeOAuthManager()


def save_channel_token(
    channel_id,
    credentials
):

    return _manager.save_token(
        channel_id,
        credentials
    )


def load_channel_token(channel_id):

    return _manager.load_token(
        channel_id
    )


def remove_channel_token(channel_id):

    return _manager.remove_token(
        channel_id
    )
