# VideoApprovalController.py

from VideoPreview import create_preview
from FounderApproval import get_approval, approve, reject


class VideoApprovalController:

    def create_video_for_approval(
        self,
        video_path,
        title,
        platform="YouTube",
        description=""
    ):
        return create_preview(
            video_path=video_path,
            title=title,
            platform=platform,
            description=description
        )

    # REQUIRED
    def create_video_preview(
        self,
        video_path,
        title,
        platform="YouTube",
        description=""
    ):
        return self.create_video_for_approval(
            video_path,
            title,
            platform,
            description
        )

    def get_request(self, approval_id):
        return get_approval(approval_id)

    # REQUIRED
    def get_video_preview(self, approval_id):
        return self.get_request(approval_id)

    def approve_video(self, approval_id):

        approval = get_approval(approval_id)

        if not approval:
            return {
                "status": "FAILED",
                "message": "Approval request not found."
            }

        if approval["status"] != "PENDING":
            return {
                "status": "FAILED",
                "message": "Approval already processed.",
                "approval": approval
            }

        return approve(approval_id)

    def reject_video(self, approval_id):

        approval = get_approval(approval_id)

        if not approval:
            return {
                "status": "FAILED",
                "message": "Approval request not found."
            }

        if approval["status"] != "PENDING":
            return {
                "status": "FAILED",
                "message": "Approval already processed.",
                "approval": approval
            }

        return reject(approval_id)


_controller = VideoApprovalController()


def create_video_for_approval(
    video_path,
    title,
    platform="YouTube",
    description=""
):
    return _controller.create_video_for_approval(
        video_path,
        title,
        platform,
        description
    )


# REQUIRED
def create_video_preview(
    video_path,
    title,
    platform="YouTube",
    description=""
):
    return _controller.create_video_preview(
        video_path,
        title,
        platform,
        description
    )


def get_request(approval_id):
    return _controller.get_request(approval_id)


# REQUIRED
def get_video_preview(approval_id):
    return _controller.get_video_preview(approval_id)


def approve_video(approval_id):
    return _controller.approve_video(approval_id)


def reject_video(approval_id):
    return _controller.reject_video(approval_id)


if __name__ == "__main__":

    print("=" * 60)
    print("UDAAN AI - VIDEO APPROVAL CONTROLLER")
    print("=" * 60)

    print("create_video_preview : READY")
    print("get_video_preview    : READY")
    print("approve_video        : READY")
    print("reject_video         : READY")

    print("=" * 60)