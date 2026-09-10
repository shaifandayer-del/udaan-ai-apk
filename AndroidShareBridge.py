# AndroidShareBridge.py

import os
import json


BRIDGE_FILE = "udaan_android_share.json"


class AndroidShareBridge:

    def prepare_video_share(
        self,
        video_path,
        title,
        description="",
        platform="YouTube"
    ):

        if not video_path:

            return {
                "status": "FAILED",
                "message": "Video path missing."
            }

        if not os.path.exists(video_path):

            return {
                "status": "FILE_NOT_FOUND",
                "message": "Video file not found.",
                "video_path": video_path
            }

        share_package = {
            "action": "android.intent.action.SEND",
            "mime_type": "video/mp4",
            "video_path": video_path,
            "title": title,
            "description": description,
            "platform": platform,
            "founder_approved": True,
            "requires_final_user_confirmation": True
        }

        with open(
            BRIDGE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                share_package,
                file,
                indent=4,
                ensure_ascii=False
            )

        return {
            "status": "READY",
            "message": "Android video share package ready.",
            "bridge_file": BRIDGE_FILE,
            "share_package": share_package
        }


_bridge = AndroidShareBridge()


def prepare_video_share(
    video_path,
    title,
    description="",
    platform="YouTube"
):

    return _bridge.prepare_video_share(
        video_path,
        title,
        description,
        platform
    )


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("      UDAAN AI — ANDROID SHARE BRIDGE")
    print("=" * 60)

    test_video = "udaan_videos/demo.mp4"

    if not os.path.exists(test_video):

        print()
        print("⚠️ Test video nahi mila:")
        print(test_video)

        print()
        print(
            "Koi real MP4 path dene ke baad "
            "function actual READY state dega."
        )

    else:

        result = prepare_video_share(
            video_path=test_video,
            title="Udaan AI Demo",
            description="Udaan AI generated video",
            platform="YouTube"
        )

        print()
        print("📊 Status:")
        print(result["status"])

        print()
        print("📱 Android Action:")
        print(
            result["share_package"]["action"]
        )

        print()
        print("🎬 MIME Type:")
        print(
            result["share_package"]["mime_type"]
        )

        print()
        print("📺 Platform:")
        print(
            result["share_package"]["platform"]
        )

        print()
        print("🔐 Founder Approved:")
        print(
            result["share_package"]
            ["founder_approved"]
        )

        print()
        print("👤 Final User Confirmation:")
        print(
            result["share_package"]
            ["requires_final_user_confirmation"]
        )

        print()
        print("📁 Bridge File:")
        print(result["bridge_file"])

    print()
    print("=" * 60)
    print("✅ ANDROID SHARE BRIDGE READY")
    print("=" * 60)