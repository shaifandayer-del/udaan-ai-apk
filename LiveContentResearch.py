# ==========================================
# UDAAN AI - LIVE YOUTUBE CONTENT RESEARCH
# STEP 118
# ==========================================

import os
import requests
from datetime import datetime


YOUTUBE_API_URL = (
    "https://www.googleapis.com/youtube/v3"
)


class LiveContentResearch:

    def __init__(self):

        self.api_key = os.environ.get(
            "YOUTUBE_API_KEY",
            ""
        )

    def timestamp(self):

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def search_videos(
        self,
        query,
        max_results=10
    ):

        if not self.api_key:

            return {
                "status": "FAILED",
                "message":
                    "YOUTUBE_API_KEY missing."
            }

        try:

            response = requests.get(
                f"{YOUTUBE_API_URL}/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "order": "viewCount",
                    "maxResults": max_results,
                    "key": self.api_key
                },
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            videos = []

            for item in data.get(
                "items",
                []
            ):

                video_id = item.get(
                    "id",
                    {}
                ).get(
                    "videoId"
                )

                snippet = item.get(
                    "snippet",
                    {}
                )

                if not video_id:
                    continue

                videos.append({
                    "video_id": video_id,
                    "title": snippet.get(
                        "title",
                        ""
                    ),
                    "channel_id":
                        snippet.get(
                            "channelId"
                        ),
                    "channel":
                        snippet.get(
                            "channelTitle"
                        ),
                    "published_at":
                        snippet.get(
                            "publishedAt"
                        ),
                    "url":
                        "https://www.youtube.com/watch?v="
                        + video_id
                })

            return {
                "status": "SUCCESS",
                "query": query,
                "videos": videos,
                "researched_at":
                    self.timestamp()
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "query": query,
                "message":
                    "YouTube research failed.",
                "error": str(error)
            }

    def get_video_statistics(
        self,
        video_ids
    ):

        if not self.api_key:

            return {
                "status": "FAILED",
                "message":
                    "YOUTUBE_API_KEY missing."
            }

        if not video_ids:

            return {
                "status": "FAILED",
                "message":
                    "Video IDs missing."
            }

        try:

            response = requests.get(
                f"{YOUTUBE_API_URL}/videos",
                params={
                    "part":
                        "statistics,snippet",
                    "id":
                        ",".join(video_ids),
                    "key":
                        self.api_key
                },
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            results = []

            for item in data.get(
                "items",
                []
            ):

                statistics = item.get(
                    "statistics",
                    {}
                )

                snippet = item.get(
                    "snippet",
                    {}
                )

                results.append({
                    "video_id":
                        item.get("id"),
                    "title":
                        snippet.get(
                            "title",
                            ""
                        ),
                    "channel":
                        snippet.get(
                            "channelTitle"
                        ),
                    "views":
                        int(
                            statistics.get(
                                "viewCount",
                                0
                            )
                        ),
                    "likes":
                        int(
                            statistics.get(
                                "likeCount",
                                0
                            )
                        ),
                    "comments":
                        int(
                            statistics.get(
                                "commentCount",
                                0
                            )
                        ),
                    "url":
                        "https://www.youtube.com/watch?v="
                        + str(
                            item.get("id")
                        )
                })

            return {
                "status": "SUCCESS",
                "videos": results,
                "researched_at":
                    self.timestamp()
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "message":
                    "Video statistics failed.",
                "error": str(error)
            }

    def research_topic(
        self,
        query,
        max_results=10
    ):

        search_result = self.search_videos(
            query,
            max_results
        )

        if search_result.get(
            "status"
        ) != "SUCCESS":

            return search_result

        videos = search_result.get(
            "videos",
            []
        )

        video_ids = [
            video["video_id"]
            for video in videos
            if video.get("video_id")
        ]

        statistics = (
            self.get_video_statistics(
                video_ids
            )
        )

        if statistics.get(
            "status"
        ) != "SUCCESS":

            return statistics

        ranked = []

        for video in statistics.get(
            "videos",
            []
        ):

            score = (
                video["views"]
                + video["likes"] * 5
                + video["comments"] * 10
            )

            video["score"] = score

            ranked.append(video)

        ranked.sort(
            key=lambda item:
                item.get("score", 0),
            reverse=True
        )

        return {
            "status": "SUCCESS",
            "agent": "Research AI",
            "query": query,
            "total_results": len(ranked),
            "best_content": ranked,
            "researched_at":
                self.timestamp()
        }


_research = LiveContentResearch()


def search_youtube(
    query,
    max_results=10
):

    return _research.search_videos(
        query,
        max_results
    )


def research_topic(
    query,
    max_results=10
):

    return _research.research_topic(
        query,
        max_results
    )


def get_video_statistics(
    video_ids
):

    return _research.get_video_statistics(
        video_ids
    )
