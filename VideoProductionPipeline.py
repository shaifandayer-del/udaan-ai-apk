
import datetime
import os
import re
import shutil
import subprocess
import uuid


class VideoProductionPipeline:
    def __init__(self, base_dir="udaan_videos"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _duration(self, command):
        text = str(command or "").lower()

        match = re.search(
            r"(\d+)\s*(?:sec|secs|second|seconds)",
            text
        )

        if match:
            return max(5, min(int(match.group(1)), 300))

        match = re.search(
            r"(\d+)\s*(?:min|mins|minute|minutes)",
            text
        )

        if match:
            return max(
                5,
                min(int(match.group(1)) * 60, 600)
            )

        return 10

    def _find_ffmpeg(self):
        return (
            shutil.which("ffmpeg")
            or "/usr/bin/ffmpeg"
            if os.path.exists("/usr/bin/ffmpeg")
            else shutil.which("ffmpeg")
        )

    def _render_mp4(
        self,
        output_path,
        command,
        duration
    ):
        ffmpeg = self._find_ffmpeg()

        if not ffmpeg:
            raise RuntimeError(
                "FFmpeg is not installed on the server."
            )

        title = str(command or "UDAAN AI VIDEO")
        title = title.replace("'", "")
        title = title.replace(":", "\\:")
        title = title[:70]

        font = (
            "/usr/share/fonts/truetype/"
            "dejavu/DejaVuSans-Bold.ttf"
        )

        video_filter = (
            "drawtext="
            f"fontfile={font}:"
            f"text='{title}':"
            "fontcolor=white:"
            "fontsize=34:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2:"
            "box=1:"
            "boxcolor=black@0.45:"
            "boxborderw=20"
        )

        command_args = [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            (
                "color="
                "c=0x061D42:"
                "s=720x1280:"
                "r=30:"
                f"d={duration}"
            ),
            "-vf",
            video_filter,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            output_path
        ]

        process = subprocess.run(
            command_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=max(120, duration * 15)
        )

        if process.returncode != 0:
            fallback_args = [
                ffmpeg,
                "-y",
                "-f",
                "lavfi",
                "-i",
                (
                    "color="
                    "c=0x061D42:"
                    "s=720x1280:"
                    "r=30:"
                    f"d={duration}"
                ),
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                output_path
            ]

            fallback = subprocess.run(
                fallback_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=max(120, duration * 15)
            )

            if fallback.returncode != 0:
                raise RuntimeError(
                    fallback.stderr[-2000:]
                )

        if not os.path.exists(output_path):
            raise RuntimeError(
                "FFmpeg finished but MP4 was not created."
            )

        if os.path.getsize(output_path) < 10000:
            raise RuntimeError(
                "Generated MP4 is invalid or empty."
            )

        return output_path

    def create_video_project(self, command):
        command = str(command or "").strip()

        if not command:
            return {
                "status": "FAILED",
                "message": "Video command is empty."
            }

        timestamp = datetime.datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        project_id = (
            f"video_{timestamp}_{uuid.uuid4().hex[:6]}"
        )

        project_path = os.path.join(
            self.base_dir,
            project_id
        )

        os.makedirs(
            project_path,
            exist_ok=True
        )

        video_path = os.path.join(
            project_path,
            "udaan_ai_video.mp4"
        )

        duration = self._duration(command)

        metadata_path = os.path.join(
            project_path,
            "project.txt"
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(
                "UDAAN AI VIDEO PROJECT\n"
                f"Project ID: {project_id}\n"
                f"Command: {command}\n"
                f"Duration: {duration} seconds\n"
                f"Created: "
                f"{datetime.datetime.now().isoformat()}\n"
            )

        try:
            self._render_mp4(
                video_path,
                command,
                duration
            )

            return {
                "status": "SUCCESS",
                "message": "Actual MP4 video generated.",
                "project_id": project_id,
                "project_path": project_path,
                "video_path": video_path,
                "video_file": os.path.basename(
                    video_path
                ),
                "duration": duration,
                "video_type": "VIDEO",
                "created_at":
                    datetime.datetime.now().isoformat()
            }

        except Exception as error:
            return {
                "status": "FAILED",
                "message": str(error),
                "project_id": project_id,
                "project_path": project_path,
                "video_path": None,
                "video_type": "VIDEO",
                "created_at":
                    datetime.datetime.now().isoformat()
            }


video_pipeline = VideoProductionPipeline()


def create_video_project(command):
    return video_pipeline.create_video_project(
        command
    )


if __name__ == "__main__":
    result = create_video_project(
        "UDAAN AI test video"
    )

    print(result)
