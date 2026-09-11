Step 125 — File name: ContentVideoOrchestrator.py

# ==========================================
# UDAAN AI - CONTENT VIDEO ORCHESTRATOR
# STEP 125
# ==========================================

from YouTubeResearchManager import get_best_content
from ContentStrategyEngine import create_strategy_from_research
from VideoProductionPipeline import create_video_job


class ContentVideoOrchestrator:

    def create_from_best_content(
        self,
        channel=None,
        max_results=5
    ):

        research = get_best_content(
            max_results
        )

        if research.get("status") != "SUCCESS":
            return research

        best_content = research.get(
            "best_content",
            []
        )

        if not best_content:
            return {
                "status": "NO_CONTENT",
                "message": "Best content nahi mila."
            }

        jobs = []

        for item in best_content:

            target_channel = (
                channel
                or item.get("target_channel")
            )

            strategy = create_strategy_from_research(
                item,
                target_channel
            )

            if strategy.get("status") != "SUCCESS":
                continue

            strategy_data = strategy.get(
                "strategy",
                {}
            )

            job = create_video_job(
                topic=strategy_data.get(
                    "topic",
                    item.get("title", "")
                ),
                channel=target_channel,
                duration=strategy_data.get(
                    "duration",
                    "60 seconds"
                ),
                language=strategy_data.get(
                    "language",
                    "Hindi"
                )
            )

            jobs.append({
                "research": item,
                "strategy": strategy,
                "video_job": job
            })

        return {
            "status": "SUCCESS",
            "agent": "Main AI",
            "total_jobs": len(jobs),
            "pipeline": jobs
        }


_orchestrator = ContentVideoOrchestrator()


def create_content_videos(
    channel=None,
    max_results=5
):

    return _orchestrator.create_from_best_content(
        channel,
        max_results
    )
