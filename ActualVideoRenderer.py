# ==========================================
# UDAAN AI - ACTUAL VIDEO RENDERER
# STEP 131
# ==========================================

import os
import subprocess
from datetime import datetime


class ActualVideoRenderer:

    def __init__(self, output_dir="udaan_videos"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def render_video(
        self,
        image_path,
        audio_path,
        output_name=None
    ):

        if not image_path or not os.path.exists(image_path):
            return {
                "status": "FAILED",
                "message": "Image file not found."
            }

        if not audio_path or not os.path.exists(audio_path):
            return {
                "status": "FAILED",
                "message": "Audio file not found."
            }

        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"udaan_video_{timestamp}.mp4"

        output_path = os.path.join(
            self.output_dir,
            output_name
        )

        command = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            image_path,
            "-i",
            audio_path,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            output_path
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                return {
                    "status": "FAILED",
                    "message": "Video rendering failed.",
                    "error": result.stderr[-2000:]
                }

            if not os.path.exists(output_path):

                return {
                    "status": "FAILED",
                    "message": "Video file was not created."
                }

            return {
                "status": "SUCCESS",
                "video_path": output_path,
                "message": "Video rendered successfully."
            }

        except FileNotFoundError:

            return {
                "status": "FAILED",
                "message": "FFmpeg is not installed on the server."
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "message": "Unexpected video rendering error.",
                "error": str(error)
            }


_renderer = ActualVideoRenderer()


def render_video(
    image_path,
    audio_path,
    output_name=None
):

    return _renderer.render_video(
        image_path=image_path,
        audio_path=audio_path,
        output_name=output_name
    )
