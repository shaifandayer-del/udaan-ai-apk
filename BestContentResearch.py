# ==========================================
# UDAAN AI - BEST CONTENT RESEARCH ENGINE
# STEP 117
# ==========================================

from datetime import datetime


class BestContentResearch:

    def __init__(self):
        self.results = []

    def timestamp(self):
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def add_result(
        self,
        channel,
        title,
        views=0,
        likes=0,
        comments=0,
        url=None,
        category=None
    ):

        item = {
            "channel": str(channel),
            "title": str(title),
            "views": int(views or 0),
            "likes": int(likes or 0),
            "comments": int(comments or 0),
            "url": url,
            "category": category,
            "researched_at": self.timestamp()
        }

        item["score"] = self.calculate_score(item)

        self.results.append(item)

        return item

    def calculate_score(self, item):

        views = item.get("views", 0)
        likes = item.get("likes", 0)
        comments = item.get("comments", 0)

        return (
            views
            + (likes * 5)
            + (comments * 10)
        )

    def get_best_content(self, limit=10):

        sorted_results = sorted(
            self.results,
            key=lambda item: item.get("score", 0),
            reverse=True
        )

        return sorted_results[:limit]

    def get_channel_results(self, channel):

        return [
            item
            for item in self.results
            if item.get("channel") == channel
        ]

    def clear_results(self):

        self.results = []

        return {
            "status": "SUCCESS",
            "message": "Research results cleared."
        }

    def research_summary(self):

        best = self.get_best_content(5)

        return {
            "status": "SUCCESS",
            "agent": "Research AI",
            "total_results": len(self.results),
            "best_content": best,
            "researched_at": self.timestamp()
        }


_research_engine = BestContentResearch()


def add_research_result(
    channel,
    title,
    views=0,
    likes=0,
    comments=0,
    url=None,
    category=None
):

    return _research_engine.add_result(
        channel,
        title,
        views,
        likes,
        comments,
        url,
        category
    )


def get_best_content(limit=10):

    return _research_engine.get_best_content(
        limit
    )


def get_channel_results(channel):

    return _research_engine.get_channel_results(
        channel
    )


def research_summary():

    return _research_engine.research_summary()
