# ==========================================
# UDAAN AI - CONTENT STRATEGY ENGINE
# STEP 120
# ==========================================

from datetime import datetime


class ContentStrategyEngine:

    def __init__(self):
        self.strategies = []

    def timestamp(self):
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def create_strategy(
        self,
        topic,
        channel=None,
        content_type="video",
        language="Hindi",
        duration="60 seconds"
    ):

        topic = str(topic or "").strip()

        if not topic:
            return {
                "status": "FAILED",
                "message": "Topic empty hai."
            }

        strategy = {
            "topic": topic,
            "channel": channel,
            "content_type": content_type,
            "language": language,
            "duration": duration,
            "created_at": self.timestamp(),

            "content_plan": {
                "hook": (
                    "First 3 seconds mein strong attention hook."
                ),
                "main_content": (
                    "Topic ko clear aur engaging way mein explain karo."
                ),
                "value": (
                    "Viewer ko useful information ya solution do."
                ),
                "call_to_action": (
                    "Like, subscribe aur next video ke liye CTA."
                )
            },

            "production": {
                "script": "GENERATE_WITH_CONTENT_AI",
                "voice": "GENERATE_WITH_VIDEO_AI",
                "visuals": "GENERATE_WITH_VIDEO_AI",
                "subtitles": "AUTO",
                "thumbnail": "GENERATE_WITH_CREATIVE_AI"
            },

            "workflow": [
                "RESEARCH",
                "TOPIC_SELECTION",
                "SCRIPT",
                "CONTENT_REVIEW",
                "VIDEO_CREATION",
                "VIDEO_PREVIEW",
                "FOUNDER_APPROVAL",
                "UPLOAD"
            ],

            "founder_approval_required": True
        }

        self.strategies.append(strategy)

        return {
            "status": "SUCCESS",
            "agent": "Content AI",
            "strategy": strategy
        }

    def create_from_research(
        self,
        research_item,
        channel=None
    ):

        if not research_item:
            return {
                "status": "FAILED",
                "message": "Research result missing."
            }

        topic = research_item.get(
            "title",
            research_item.get(
                "topic",
                ""
            )
        )

        return self.create_strategy(
            topic=topic,
            channel=channel,
            content_type="video"
        )

    def get_strategies(self):

        return {
            "status": "SUCCESS",
            "total": len(self.strategies),
            "strategies": self.strategies
        }

    def get_latest(self):

        if not self.strategies:
            return {
                "status": "EMPTY",
                "message": "No content strategy available."
            }

        return {
            "status": "SUCCESS",
            "strategy": self.strategies[-1]
        }


_engine = ContentStrategyEngine()


def create_content_strategy(
    topic,
    channel=None,
    content_type="video",
    language="Hindi",
    duration="60 seconds"
):

    return _engine.create_strategy(
        topic,
        channel,
        content_type,
        language,
        duration
    )


def create_strategy_from_research(
    research_item,
    channel=None
):

    return _engine.create_from_research(
        research_item,
        channel
    )


def get_content_strategies():

    return _engine.get_strategies()


def get_latest_strategy():

    return _engine.get_latest()
