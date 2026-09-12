import os
import subprocess
import shutil
import tempfile
from pathlib import Path


VIDEO_DIR = Path("generated_videos")


def _find_ffmpeg():
    return shutil.which("ffmpeg")


def _prepare_script(script):
    if not script:
        return "UDAAN AI VIDEO"

    return str(script).strip()


def _create_text_video(script, title, output_path):
    ffmpeg = _find_ffmpeg()

    if not ffmpeg:
        return {
            "status": "FAILED",
            "message": "FFmpeg installed nahi hai."
        }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text = _prepare_script(script)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8"
    ) as file:
        file.write(text)
        text_file = file.name

    try:
        command = [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=0x07070F:s=1080x1920:r=30",
            "-vf",
            (
                "drawtext="
                "fontcolor=white:"
                "fontsize=52:"
                "x=(w-text_w)/2:"
                "y=(h-text_h)/2:"
                f"textfile='{text_file}':"
                "line_spacing=12"
            ),
            "-t",
            "30",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_path)
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return {
                "status": "FAILED",
                "message": "FFmpeg video rendering failed.",
                "error": result.stderr[-3000:]
            }

        if not output_path.exists() or output_path.stat().st_size == 0:
            return {
                "status": "FAILED",
                "message": "Final MP4 create nahi hui."
            }

        return {
            "status": "SUCCESS",
            "message": "Final video render completed.",
            "title": title,
            "video_path": str(output_path),
            "output_path": str(output_path),
            "format": "mp4"
        }

    finally:
        try:
            os.remove(text_file)
        except OSError:
            pass


def render_video(
    script="",
    title="UDAAN AI Video",
    output_path=None
):
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        output_path = VIDEO_DIR / "final_video.mp4"

    return _create_text_video(
        script,
        title,
        output_path
    )


def create_video(
    script="",
    title="UDAAN AI Video",
    output_path=None
):
    return render_video(
        script=script,
        title=title,
        output_path=output_path
    )


def generate_video(
    script="",
    title="UDAAN AI Video",
    output_path=None
):
    return render_video(
        script=script,
        title=title,
        output_path=output_path
    )


def render(
    script="",
    title="UDAAN AI Video",
    output_path=None
):
    return render_video(
        script=script,
        title=title,
        output_path=output_path
    )


def run(
    script="",
    title="UDAAN AI Video",
    output_path=None
):
    return render_video(
        script=script,
        title=title,
        output_path=output_path
    )


def execute(
    script="",
    title="UDAAN AI Video",
    output_path=None
):
    return render_video(
        script=script,
        title=title,
        output_path=output_path
    )
