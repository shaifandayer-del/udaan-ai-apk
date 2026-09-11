# ==========================================
# UDAAN AI - MULTI CHANNEL UPLOAD MANAGER
# STEP 124
# ==========================================

from YouTubePublishEngine import publish_video


class MultiChannelUploadManager:

    def __init__(self):
        self.channels = {}

    def add_channel(
        self,
        channel_name,
        channel_id=None,
        enabled=True
    ):

        if not channel_name:
            return {
                "status": "FAILED",
                "message": "Channel name missing."
            }

        self.channels[channel_name] = {
            "channel_name": channel_name,
            "channel_id": channel_id,
            "enabled": bool(enabled)
        }

        return {
            "status": "SUCCESS",
            "channel": self.channels[channel_name]
        }

    def remove_channel(self, channel_name):

        if channel_name not in self.channels:
            return {
                "status": "FAILED",
                "message": "Channel not found."
            }

        del self.channels[channel_name]

        return {
            "status": "SUCCESS",
            "message": "Channel removed."
        }

    def list_channels(self):

        return {
            "status": "SUCCESS",
            "total_channels": len(self.channels),
            "channels": list(
                self.channels.values()
            )
        }

    def upload_to_channel(
        self,
        channel_name,
        video_path,
        title,
        description="",
        tags=None,
        privacy_status="private"
    ):

        channel = self.channels.get(
            channel_name
        )

        if not channel:
            return {
                "status": "FAILED",
                "message": "Channel not registered."
            }

        if not channel.get("enabled"):
            return {
                "status": "FAILED",
                "message": "Channel is disabled."
            }

        result = publish_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status=privacy_status
        )

        return {
            "status": result.get(
                "status",
                "FAILED"
            ),
            "channel": channel_name,
            "channel_id":
                channel.get("channel_id"),
            "upload_result": result
        }

    def upload_to_all_channels(
        self,
        video_path,
        title,
        description="",
        tags=None,
        privacy_status="private"
    ):

        results = []

        for channel_name, channel in (
            self.channels.items()
        ):

            if not channel.get("enabled"):
                continue

            result = self.upload_to_channel(
                channel_name=channel_name,
                video_path=video_path,
                title=title,
                description=description,
                tags=tags,
                privacy_status=privacy_status
            )

            results.append(result)

        return {
            "status": "SUCCESS",
            "total_channels": len(results),
            "results": results
        }


_manager = MultiChannelUploadManager()


def add_channel(
    channel_name,
    channel_id=None,
    enabled=True
):

    return _manager.add_channel(
        channel_name,
        channel_id,
        enabled
    )


def remove_channel(channel_name):

    return _manager.remove_channel(
        channel_name
    )


def list_channels():

    return _manager.list_channels()


def upload_to_channel(
    channel_name,
    video_path,
    title,
    description="",
    tags=None,
    privacy_status="private"
):

    return _manager.upload_to_channel(
        channel_name,
        video_path,
        title,
        description,
        tags,
        privacy_status
    )


def upload_to_all_channels(
    video_path,
    title,
    description="",
    tags=None,
    privacy_status="private"
):

    return _manager.upload_to_all_channels(
        video_path,
        title,
        description,
        tags,
        privacy_status
    )
