"""
UDAAN X AI
Central Orchestrator

Founder
   ↓
Orchestrator
   ↓
Correct AI Agent
   ↓
Task
   ↓
Result
"""

from agents.ceo import create_ceo
from agents.research import create_research
from agents.content import create_content
from agents.creative import create_creative
from agents.video import create_video
from agents.social import create_social
from agents.youtube import create_youtube
from agents.analytics import create_analytics
from agents.marketing import create_marketing
from agents.developer import create_developer
from agents.automation import create_automation


class Orchestrator:
    def __init__(self):
        self.ceo = create_ceo()
        self.research = create_research()
        self.content = create_content()
        self.creative = create_creative()
        self.video = create_video()
        self.social = create_social()
        self.youtube = create_youtube()
        self.analytics = create_analytics()
        self.marketing = create_marketing()
        self.developer = create_developer()
        self.automation = create_automation()

    def route_command(self, command):
        command_lower = command.lower()

        if any(word in command_lower for word in [
            "research", "research karo", "trend", "competitor"
        ]):
            return "Research AI"

        if any(word in command_lower for word in [
            "script", "content", "reel idea", "post idea"
        ]):
            return "Content AI"

        if any(word in command_lower for word in [
            "thumbnail", "visual", "creative", "design"
        ]):
            return "Creative AI"

        if any(word in command_lower for word in [
            "video", "reel banao", "video banao"
        ]):
            return "Video AI"

        if any(word in command_lower for word in [
            "instagram", "social media", "instagram post"
        ]):
            return "Social AI"

        if any(word in command_lower for word in [
            "youtube", "youtube video", "youtube channel"
        ]):
            return "YouTube AI"

        if any(word in command_lower for word in [
            "analytics", "views", "retention", "performance"
        ]):
            return "Analytics AI"

        if any(word in command_lower for word in [
            "marketing", "campaign", "growth", "promotion"
        ]):
            return "Marketing AI"

        if any(word in command_lower for word in [
            "code", "coding", "app banao", "developer", "bug"
        ]):
            return "Developer AI"

        if any(word in command_lower for word in [
            "automation", "automate", "automatic", "repeat"
        ]):
            return "Automation AI"

        return "CEO AI"

    def execute(self, command):
        command = command.strip()

        if not command:
            return {
                "status": "error",
                "message": "Founder command empty hai."
            }

        assigned_agent = self.route_command(command)

        return {
            "status": "assigned",
            "founder_command": command,
            "assigned_agent": assigned_agent,
            "message": f"{assigned_agent} ko task assign kiya gaya."
        }


def create_orchestrator():
    return Orchestrator()