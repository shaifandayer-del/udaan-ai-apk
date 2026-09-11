# ==========================================
# UDAAN AI - YOUTUBE RESEARCH MANAGER
# STEP 119
# ==========================================

from LiveContentResearch import research_topic


class YouTubeResearchManager:

    def __init__(self):
        self.channels = []

    def add_channel(self, channel_name, niche):
        channel = {
            "channel": channel_name,
            "niche": niche,
            "active": True
        }

        self.channels.append(channel)

        return {
            "status": "SUCCESS",
            "channel": channel
        }

    def remove_channel(self, channel_name):

        self.channels = [
            channel
            for channel in self.channels
            if channel["channel"] != channel_name
        ]

        return {
            "status": "SUCCESS",
            "message": "Channel removed."
        }

    def list_channels(self):

        return {
            "status": "SUCCESS",
            "total_channels": len(self.channels),
            "channels": self.channels
        }

    def research_all_channels(self, max_results=10):

        results = []

        for channel in self.channels:

            if not channel.get("active"):
                continue

            result = research_topic(
                channel["niche"],
                max_results
            )

            results.append({
                "channel": channel["channel"],
                "niche": channel["niche"],
                "research": result
            })

        return {
            "status": "SUCCESS",
            "total_channels": len(results),
            "results": results
        }

    def best_content(self, max_results=5):

        research = self.research_all_channels(
            max_results
        )

        all_content = []

        for channel_result in research["results"]:

            content = channel_result[
                "research"
            ].get(
                "best_content",
                []
            )

            for item in content:

                item["target_channel"] = (
                    channel_result["channel"]
                )

                all_content.append(item)

        all_content.sort(
            key=lambda item:
                item.get("score", 0),
            reverse=True
        )

        return {
            "status": "SUCCESS",
            "best_content":
                all_content[:max_results]
        }


_manager = YouTubeResearchManager()


def add_research_channel(
    channel_name,
    niche
):

    return _manager.add_channel(
        channel_name,
        niche
    )


def remove_research_channel(
    channel_name
):

    return _manager.remove_channel(
        channel_name
    )


def list_research_channels():

    return _manager.list_channels()


def research_channels(
    max_results=10
):

    return _manager.research_all_channels(
        max_results
    )


def get_best_content(
    max_results=5
):

    return _manager.best_content(
        max_results
    )
