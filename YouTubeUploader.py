# YouTubeUploader.py

import os

from FounderApproval import get_approval


YOUTUBE_UPLOAD_SCOPE = (
    "https://www.googleapis.com/auth/youtube.upload"
)


class YouTubeUploader:

    def check_ready(self, approval_id):

        approval = get_approval(
            approval_id
        )

        if not approval:

            return {
                "status": "FAILED",
                "message": "Approval request not found."
            }

        if approval.get("status") != "APPROVED":

            return {
                "status": "BLOCKED",
                "message": (
                    "Founder approval required "
                    "before YouTube upload."
                )
            }

        file_path = approval.get(
            "file_path"
        )

        if not file_path:

            return {
                "status": "FAILED",
                "message": "Video file path missing."
            }

        if not os.path.exists(file_path):

            return {
                "status": "FILE_NOT_FOUND",
                "message": "Video file does not exist.",
                "file_path": file_path
            }

        return {
            "status": "READY",
            "message": (
                "Founder approval verified. "
                "Video is ready for YouTube OAuth upload."
            ),
            "approval_id": approval_id,
            "file_path": file_path,
            "title": approval.get("title"),
            "description": approval.get("description"),
            "oauth_scope": YOUTUBE_UPLOAD_SCOPE
        }


_uploader = YouTubeUploader()


def check_youtube_upload_ready(
    approval_id
):

    return _uploader.check_ready(
        approval_id
    )


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — YOUTUBE UPLOADER")
    print("=" * 60)

    print()
    print("🔐 Required OAuth scope:")
    print(YOUTUBE_UPLOAD_SCOPE)

    print()
    print("🛡️ SAFE MODE:")
    print("Real YouTube upload is disabled in this step.")

    print()
    print("ℹ️ Upload will only be enabled after:")
    print("1. Founder approval")
    print("2. Video file verification")
    print("3. YouTube OAuth connection")

    print()
    print("=" * 60)
    print("✅ YOUTUBE UPLOADER FOUNDATION READY")
    print("=" * 60)