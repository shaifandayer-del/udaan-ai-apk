import os
import time
import json

from FounderApproval import request_approval


PREVIEW_DIR = "udaan_previews"


def create_preview(
    video_path,
    title,
    platform="YouTube",
    description=""
):

    os.makedirs(
        PREVIEW_DIR,
        exist_ok=True
    )

    preview_id = "PREVIEW-" + str(
        int(time.time() * 1000)
    )

    preview_file = os.path.join(
        PREVIEW_DIR,
        preview_id + ".json"
    )

    preview = {
        "preview_id": preview_id,
        "video_path": video_path,
        "title": title,
        "platform": platform,
        "description": description,
        "status": "WAITING_FOUNDER_APPROVAL",
        "created_at": time.time()
    }

    with open(
        preview_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            preview,
            file,
            indent=4,
            ensure_ascii=False
        )

    approval = request_approval(
        action="UPLOAD_VIDEO",
        platform=platform,
        file_path=video_path,
        title=title,
        description=description
    )

    return {
        "status": "PREVIEW_READY",
        "preview": preview,
        "preview_file": preview_file,
        "approval": approval
    }


def get_preview(preview_id):

    preview_file = os.path.join(
        PREVIEW_DIR,
        preview_id + ".json"
    )

    if not os.path.exists(preview_file):

        return None

    with open(
        preview_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — VIDEO PREVIEW SYSTEM")
    print("=" * 60)

    result = create_preview(
        video_path="udaan_videos/demo.mp4",
        title="Udaan AI Demo",
        platform="YouTube",
        description="Founder preview test"
    )

    print()
    print("🎬 VIDEO:")
    print(result["preview"]["video_path"])

    print()
    print("📝 TITLE:")
    print(result["preview"]["title"])

    print()
    print("📺 PLATFORM:")
    print(result["preview"]["platform"])

    print()
    print("👀 PREVIEW STATUS:")
    print(result["status"])

    print()
    print("🆔 PREVIEW ID:")
    print(result["preview"]["preview_id"])

    print()
    print("🔐 APPROVAL ID:")
    print(result["approval"]["approval_id"])

    print()
    print("📁 Preview File:")
    print(result["preview_file"])

    print()
    print("⏳ Waiting for Founder Approval...")

    print()
    print("=" * 60)
    print("✅ VIDEO PREVIEW SYSTEM READY")
    print("=" * 60)