# ==========================================
# UDAAN AI - AUTOMATION CONTROLLER
# STEP 129
# ==========================================

from UdaanProductionPipeline import run_production_pipeline
from ApprovedUploadRunner import run_approved_uploads


class UdaanAutomationController:

    def run_research_pipeline(
        self,
        channel=None,
        max_results=5
    ):

        return run_production_pipeline(
            channel=channel,
            max_results=max_results
        )

    def run_approved_uploads(self):

        return run_approved_uploads()

    def run_cycle(
        self,
        channel=None,
        max_results=5
    ):

        production = self.run_research_pipeline(
            channel=channel,
            max_results=max_results
        )

        if production.get("status") != "SUCCESS":
            return production

        return {
            "status": "SUCCESS",
            "production": production,
            "upload": {
                "status": "WAITING_FOUNDER_APPROVAL",
                "message":
                    "Videos approval ke baad hi upload honge."
            }
        }


_controller = UdaanAutomationController()


def run_automation_cycle(
    channel=None,
    max_results=5
):

    return _controller.run_cycle(
        channel,
        max_results
    )


def run_approved_upload_cycle():

    return _controller.run_approved_uploads()
