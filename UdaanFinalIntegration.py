# ==========================================
# UDAAN AI - FINAL INTEGRATION
# STEP 137
# ==========================================

from UdaanAutomationController import (
    run_automation_cycle,
    run_approved_upload_cycle
)
from UdaanNotificationManager import (
    notify,
    get_unread_notifications
)
from PersistentUploadScheduler import (
    get_pending_uploads
)


class UdaanFinalIntegration:

    def system_status(self):

        return {
            "status": "ONLINE",
            "system": "UDAAN AI",
            "modules": {
                "automation": "READY",
                "video_pipeline": "READY",
                "founder_approval": "ENABLED",
                "persistent_scheduler": "READY",
                "youtube": "READY",
                "instagram": "READY",
                "notifications": "READY",
                "multi_channel": "READY"
            }
        }

    def run_production(
        self,
        channel=None,
        max_results=5
    ):

        result = run_automation_cycle(
            channel=channel,
            max_results=max_results
        )

        if result.get("status") == "SUCCESS":

            notify(
                "UDAAN AI",
                "Production pipeline completed.",
                "SUCCESS"
            )

        else:

            notify(
                "UDAAN AI",
                "Production pipeline failed.",
                "ERROR"
            )

        return result

    def run_approved_uploads(self):

        result = run_approved_upload_cycle()

        notify(
            "UDAAN AI",
            "Approved upload cycle completed.",
            "UPLOAD"
        )

        return result

    def dashboard(self):

        return {
            "status": self.system_status(),
            "pending_uploads": get_pending_uploads(),
            "notifications": get_unread_notifications()
        }


_integration = UdaanFinalIntegration()


def get_final_system_status():

    return _integration.system_status()


def run_final_production(
    channel=None,
    max_results=5
):

    return _integration.run_production(
        channel,
        max_results
    )


def run_final_approved_uploads():

    return _integration.run_approved_uploads()


def get_udaan_dashboard():

    return _integration.dashboard()
