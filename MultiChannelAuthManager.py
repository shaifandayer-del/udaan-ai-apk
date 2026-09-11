# ==========================================
# UDAAN AI - MULTI CHANNEL AUTH MANAGER
# STEP 136
# ==========================================

import os
from YouTubeOAuthManager import (
    save_channel_token,
    load_channel_token,
    remove_channel_token
)


class MultiChannelAuthManager:

    def __init__(self):
        self.channels = {}

    def register_channel(
        self,
        channel_id,
        channel_name
    ):

        channel_id = str(channel_id)

        self.channels[channel_id] = {
            "channel_id": channel_id,
            "channel_name": str(channel_name),
            "enabled": True
        }

        return {
            "status": "SUCCESS",
            "channel": self.channels[channel_id]
        }

    def remove_channel(self, channel_id):

        channel_id = str(channel_id)

        self.channels.pop(
            channel_id,
            None
        )

        remove_channel_token(
            channel_id
        )

        return {
            "status": "SUCCESS",
            "channel_id": channel_id
        }

    def list_channels(self):

        return {
            "status": "SUCCESS",
            "channels": list(
                self.channels.values()
            )
        }

    def save_credentials(
        self,
        channel_id,
        credentials
    ):

        channel_id = str(channel_id)

        if channel_id not in self.channels:
            return {
                "status": "FAILED",
                "message": "Channel is not registered."
            }

        return save_channel_token(
            channel_id,
            credentials
        )

    def load_credentials(
        self,
        channel_id
    ):

        return load_channel_token(
            str(channel_id)
        )

    def enable_channel(
        self,
        channel_id
    ):

        channel_id = str(channel_id)

        if channel_id not in self.channels:
            return {
                "status": "FAILED",
                "message": "Channel is not registered."
            }

        self.channels[channel_id]["enabled"] = True

        return {
            "status": "SUCCESS",
            "channel_id": channel_id,
            "enabled": True
        }

    def disable_channel(
        self,
        channel_id
    ):

        channel_id = str(channel_id)

        if channel_id not in self.channels:
            return {
                "status": "FAILED",
                "message": "Channel is not registered."
            }

        self.channels[channel_id]["enabled"] = False

        return {
            "status": "SUCCESS",
            "channel_id": channel_id,
            "enabled": False
        }


_manager = MultiChannelAuthManager()


def register_channel(
    channel_id,
    channel_name
):

    return _manager.register_channel(
        channel_id,
        channel_name
    )


def remove_channel(channel_id):

    return _manager.remove_channel(
        channel_id
    )


def list_channels():

    return _manager.list_channels()


def save_channel_credentials(
    channel_id,
    credentials
):

    return _manager.save_credentials(
        channel_id,
        credentials
    )


def load_channel_credentials(
    channel_id
):

    return _manager.load_credentials(
        channel_id
    )
