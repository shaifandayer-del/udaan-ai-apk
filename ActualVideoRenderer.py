import os
import shutil
import subprocess
import datetime


class ActualVideoRenderer:

    def __init__(self, output_dir="udaan_videos"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _ffmpeg(self):
        return shutil.which("ffmpeg")

    def _safe_text(self, text):
        text = str(text or "UDAAN AI")
        return (
            text.replace("\\", "")
            .replace("'", "")
            .replace(":", "\\:")
            .replace("\n", " ")
        )[:80]

    def render_video(
        self,
        project_path,
        title="UDAAN AI",
        duration=10
    ):
        project_path = str(project_path or "").strip()

        if not project_path:
            return {
                "status": "FAILED",
                "message": "Project path is missing."
            }

        os.makedirs(project_path, exist_ok=True)

        ffmpeg = self._ffmpeg()

        if not ffmpeg:
            return {
                "status": "FAILED",
                "message": "FFmpeg is not installed."
            }

        try:
            duration = max(
                5,
                min(int(duration), 600)
            )
        except Exception:
            duration = 10

        output_path = os.path.join(
            project_path,
            "udaan_ai_video.mp4"
        )

        safe_title = self._safe_text(title)

        video_filter = (
            "drawtext="
            "fontfile=/usr/share/fonts/truetype/"
            "dejavu/DejaVuSans-Bold.ttf:"
            f"text='{safe_title}':"
            "fontcolor=white:"
            "fontsize=38:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2:"
            "box=1:"
            "boxcolor=black@0.45:"
            "boxborderw=18"
        )

        command = [
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

        try:
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=max(
                    120,
                    duration * 15
                )
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "FAILED",
                "message": "Video rendering timed out."
            }
        except Exception as error:
            return {
                "status": "FAILED",
                "message": str(error)
            }

        if process.returncode != 0:
            return {
                "status": "FAILED",
                "message": process.stderr[-3000:]
            }

        if not os.path.isfile(output_path):
            return {
                "status": "FAILED",
                "message": "MP4 file was not created."
            }

        file_size = os.path.getsize(output_path)

        if file_size < 10000:
            try:
                os.remove(output_path)
            except Exception:
                pass

            return {
                "status": "FAILED",
                "message": "Generated MP4 is invalid or empty."
            }

        return {
            "status": "SUCCESS",
            "message": "Video rendered successfully.",
            "video_path": output_path,
            "video_file": "udaan_ai_video.mp4",
            "duration": duration,
            "file_size": file_size,
            "rendered_at":
                datetime.datetime.now().isoformat()
        }


actual_video_renderer = ActualVideoRenderer()


def render_video(
    project_path,
    title="UDAAN AI",
    duration=10
):
    return actual_video_renderer.render_video(
        project_path,
        title,
        duration
    )
