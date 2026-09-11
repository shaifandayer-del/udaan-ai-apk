Step 134 — File name: UdaanNotificationManager.py

# ==========================================
# UDAAN AI - NOTIFICATION MANAGER
# STEP 134
# ==========================================

from datetime import datetime


class UdaanNotificationManager:

    def __init__(self):
        self.notifications = []

    def create(
        self,
        title,
        message,
        notification_type="INFO"
    ):

        notification = {
            "id": len(self.notifications) + 1,
            "title": str(title),
            "message": str(message),
            "type": str(notification_type),
            "created_at": datetime.now().isoformat(),
            "read": False
        }

        self.notifications.append(
            notification
        )

        return {
            "status": "SUCCESS",
            "notification": notification
        }

    def get_all(self):

        return {
            "status": "SUCCESS",
            "notifications": list(
                reversed(self.notifications)
            )
        }

    def get_unread(self):

        unread = [
            item
            for item in self.notifications
            if not item["read"]
        ]

        return {
            "status": "SUCCESS",
            "notifications": list(
                reversed(unread)
            )
        }

    def mark_read(self, notification_id):

        for item in self.notifications:

            if item["id"] == int(notification_id):

                item["read"] = True

                return {
                    "status": "SUCCESS",
                    "notification_id": notification_id
                }

        return {
            "status": "FAILED",
            "message": "Notification not found."
        }

    def clear(self):

        self.notifications.clear()

        return {
            "status": "SUCCESS",
            "message": "Notifications cleared."
        }


_manager = UdaanNotificationManager()


def notify(
    title,
    message,
    notification_type="INFO"
):

    return _manager.create(
        title,
        message,
        notification_type
    )


def get_notifications():

    return _manager.get_all()


def get_unread_notifications():

    return _manager.get_unread()


def mark_notification_read(
    notification_id
):

    return _manager.mark_read(
        notification_id
    )
