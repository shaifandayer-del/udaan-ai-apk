VideoShareController.py

import os
import shutil
from pathlib import Path


VIDEO_DIR = Path("generated_videos")


def _find_video(video_path=""):
    if video_path:
        path = Path(video_path)
        if path.exists() and path.is_file():
            return path

    if VIDEO_DIR.exists():
        videos = sorted(
            VIDEO_DIR.rglob("*.mp4"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if videos:
            return videos[0]

    return None


def get_video(video_path=""):
    video = _find_video(video_path)

    if video is None:
        return {
            "status": "FAILED",
            "message": "Video file nahi mili."
        }

    return {
        "status": "SUCCESS",
        "video_path": str(video),
        "file_name": video.name,
        "size_bytes": video.stat().st_size,
        "format": "mp4"
    }


def prepare_share(video_path="", destination="shared_videos"):
    video = _find_video(video_path)

    if video is None:
        return {
            "status": "FAILED",
            "message": "Share ke liye video nahi mili."
        }

    share_dir = Path(destination)
    share_dir.mkdir(parents=True, exist_ok=True)

    target = share_dir / video.name
    shutil.copy2(video, target)

    return {
        "status": "SUCCESS",
        "video_path": str(target),
        "file_name": target.name,
        "size_bytes": target.stat().st_size,
        "format": "mp4",
        "message": "Video sharing ke liye ready hai."
    }


def share_video(video_path=""):
    return prepare_share(video_path)


def run(command=""):
    return {
        "status": "SUCCESS",
        "agent": "Video Share",
        "command": command,
        "message": "Video share controller ready."
    }


def execute(command=""):
    return run(command)


def process(command=""):
    return run(command)


def handle(command=""):
    return run(command)


def run_agent(command=""):
    return run(command)
