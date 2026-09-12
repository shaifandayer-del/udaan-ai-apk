
import os
import json
import importlib
from datetime import datetime


PIPELINE_NAME = "UDAAN AI VIDEO PRODUCTION"


def _load_module(name):
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def _run_agent(agent_name, command):
    try:
        from AgentConnector import run_agent
        return run_agent(agent_name, command)
    except Exception as error:
        return {
            "status": "FAILED",
            "agent": agent_name,
            "error": f"{type(error).__name__}: {error}"
        }


def _call_renderer(script, title, output_path):
    renderer = _load_module("ActualVideoRenderer")

    if renderer is None:
        return {
            "status": "FAILED",
            "message": "ActualVideoRenderer module load nahi hua."
        }

    functions = [
        "render_video",
        "create_video",
        "generate_video",
        "render",
        "run",
        "execute"
    ]

    for name in functions:
        function = getattr(renderer, name, None)

        if not callable(function):
            continue

        calls = [
            lambda: function(
                script=script,
                title=title,
                output_path=output_path
            ),
            lambda: function(
                script,
                output_path
            ),
            lambda: function(script),
            lambda: function()
        ]

        for call in calls:
            try:
                result = call()

                if isinstance(result, dict):
                    return result

                return {
                    "status": "SUCCESS",
                    "output_path": str(result),
                    "message": "Video render completed."
                }

            except TypeError:
                continue
            except Exception as error:
                return {
                    "status": "FAILED",
                    "message": "Video rendering failed.",
                    "error": f"{type(error).__name__}: {error}"
                }

    return {
        "status": "FAILED",
        "message": "Video renderer function nahi mila."
    }


def create_video_project(command=""):
    if not command or not command.strip():
        return {
            "status": "FAILED",
            "message": "Video command empty hai."
        }

    command = command.strip()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    project_dir = os.path.join(
        "generated_videos",
        timestamp
    )

    os.makedirs(project_dir, exist_ok=True)

    research = _run_agent(
        "Research",
        f"""
Research this video topic and collect useful current information.

Founder Request:
{command}
""".strip()
    )

    if research.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "RESEARCH",
            "result": research
        }

    content = _run_agent(
        "Content",
        f"""
Create a complete video script from the research below.

Founder Request:
{command}

Research:
{json.dumps(research, ensure_ascii=False)}
""".strip()
    )

    if content.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "CONTENT",
            "research": research,
            "result": content
        }

    creative = _run_agent(
        "Creative",
        f"""
Create the visual direction, scenes, thumbnail concept and graphics plan
for this video.

Founder Request:
{command}

Script:
{json.dumps(content, ensure_ascii=False)}
""".strip()
    )

    if creative.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "CREATIVE",
            "research": research,
            "content": content,
            "result": creative
        }

    video = _run_agent(
        "Video",
        f"""
Prepare this video for production and rendering.

Founder Request:
{command}

Research:
{json.dumps(research, ensure_ascii=False)}

Content:
{json.dumps(content, ensure_ascii=False)}

Creative Plan:
{json.dumps(creative, ensure_ascii=False)}
""".strip()
    )

    if video.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "VIDEO",
            "research": research,
            "content": content,
            "creative": creative,
            "result": video
        }

    script = (
        content.get("script")
        or content.get("message")
        or content.get("result")
        or ""
    )

    title = (
        content.get("title")
        or f"UDAAN AI Video {timestamp}"
    )

    output_path = os.path.join(
        project_dir,
        "final_video.mp4"
    )

    render_result = _call_renderer(
        script=str(script),
        title=str(title),
        output_path=output_path
    )

    if render_result.get("status") != "SUCCESS":
        return {
            "status": "FAILED",
            "stage": "RENDER",
            "research": research,
            "content": content,
            "creative": creative,
            "video": video,
            "render": render_result
        }

    final_path = (
        render_result.get("output_path")
        or render_result.get("video_path")
        or output_path
    )

    return {
        "status": "SUCCESS",
        "pipeline": PIPELINE_NAME,
        "project_id": timestamp,
        "title": title,
        "video_path": final_path,
        "research": research,
        "content": content,
        "creative": creative,
        "video": video,
        "render": render_result,
        "approval_required": True,
        "approval_status": "PENDING",
        "publish_status": "WAITING_FOR_FOUNDER_APPROVAL",
        "message": "Video successfully prepared and rendered. Founder approval required before upload."
    }


def generate_video(command=""):
    return create_video_project(command)


def run(command=""):
    return create_video_project(command)


def execute(command=""):
    return create_video_project(command)


def process(command=""):
    return create_video_project(command)


def handle(command=""):
    return create_video_project(command)


def run_agent(command=""):
    return create_video_project(command)
