# ============================================================
# UDAAN X AI — CODE 2
# AI BRAIN + 11 AI TEAM
# ============================================================

import os
import json
import urllib.request
import urllib.error


APP_NAME = "UDAAN X AI"
TAGLINE = "Grow Yourself. Grow Others."


class GeminiBrain:
    """
    UDAAN X ka central AI brain.

    API key environment variable se li jayegi.
    Code ke andar API key save nahi karni hai.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def ask(self, prompt):

        if not self.api_key:
            return (
                "⚠️ Gemini API abhi configure nahi hai.\n"
                "UDAAN X ka AI structure ready hai, "
                "lekin real AI response ke liye GEMINI_API_KEY "
                "set karni hogi."
            )

        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-2.5-flash:generateContent?key="
            + self.api_key
        )

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=60
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            return result["candidates"][0]["content"]["parts"][0]["text"]

        except urllib.error.HTTPError as error:

            try:
                message = error.read().decode("utf-8")
            except Exception:
                message = str(error)

            return f"❌ Gemini API error: {message}"

        except Exception as error:

            return f"❌ AI connection error: {error}"


class AIAgent:

    def __init__(self, name, role, brain):
        self.name = name
        self.role = role
        self.brain = brain

    def work(self, founder_command):

        prompt = f"""
You are {self.name} inside UDAAN X AI.

Your role:
{self.role}

Founder command:
{founder_command}

Rules:
- Give useful, practical output.
- Do not invent real-world facts.
- Clearly say when information needs research or an API.
- Never claim an action was completed unless it actually happened.
- Never fake social media connections, views, uploads or analytics.
- Founder remains the highest authority.

Respond as the assigned UDAAN X AI employee.
"""

        return self.brain.ask(prompt)


class UdaanX:

    def __init__(self):

        self.brain = GeminiBrain()

        self.team = {

            "CEO AI": AIAgent(
                "CEO AI",
                "Strategy, planning, goals and decision support",
                self.brain
            ),

            "Research AI": AIAgent(
                "Research AI",
                "Research, trends, competitors and information analysis",
                self.brain
            ),

            "Content AI": AIAgent(
                "Content AI",
                "Content ideas, hooks, Hindi/Hinglish scripts and captions",
                self.brain
            ),

            "Creative AI": AIAgent(
                "Creative AI",
                "Visual concepts, thumbnails, branding and creative direction",
                self.brain
            ),

            "Video AI": AIAgent(
                "Video AI",
                "Video planning, scenes, voice, editing workflow and quality control",
                self.brain
            ),

            "Social AI": AIAgent(
                "Social AI",
                "Instagram, Facebook and social-media planning",
                self.brain
            ),

            "YouTube AI": AIAgent(
                "YouTube AI",
                "YouTube strategy, titles, descriptions and optimization",
                self.brain
            ),

            "Analytics AI": AIAgent(
                "Analytics AI",
                "Analytics, performance and optimization",
                self.brain
            ),

            "Marketing AI": AIAgent(
                "Marketing AI",
                "Marketing, growth and campaigns",
                self.brain
            ),

            "Developer AI": AIAgent(
                "Developer AI",
                "Coding, debugging, testing and app development",
                self.brain
            ),

            "Automation AI": AIAgent(
                "Automation AI",
                "Automation, workflows and repetitive task management",
                self.brain
            )
        }

    def choose_agent(self, command):

        text = command.lower()

        rules = {

            "Research AI": [
                "research", "research karo",
                "trend", "trends", "competitor"
            ],

            "Content AI": [
                "script", "content",
                "reel idea", "post idea",
                "caption", "hook"
            ],

            "Creative AI": [
                "thumbnail", "design",
                "visual", "creative", "logo"
            ],

            "Video AI": [
                "video", "reel banao",
                "video banao", "edit video"
            ],

            "Social AI": [
                "instagram", "facebook",
                "social media", "social"
            ],

            "YouTube AI": [
                "youtube", "youtube video",
                "youtube channel"
            ],

            "Analytics AI": [
                "analytics", "views",
                "retention", "performance",
                "engagement"
            ],

            "Marketing AI": [
                "marketing", "growth",
                "campaign", "promotion"
            ],

            "Developer AI": [
                "code", "coding",
                "developer", "app banao",
                "website banao", "bug",
                "debug"
            ],

            "Automation AI": [
                "automation", "automate",
                "automatic", "workflow"
            ]
        }

        for agent, keywords in rules.items():

            for keyword in keywords:

                if keyword in text:
                    return agent

        return "CEO AI"

    def execute(self, command):

        agent_name = self.choose_agent(command)
        agent = self.team[agent_name]

        print("\n" + "=" * 60)
        print("🧠 UDAAN X ORCHESTRATOR")
        print("=" * 60)

        print("👑 Founder:")
        print(command)

        print("\n🤖 Assigned AI:")
        print(agent.name)

        print("\n⚙️ AI is working...")

        answer = agent.work(command)

        print("\n💡 UDAAN X RESULT")
        print("-" * 60)
        print(answer)

    def start(self):

        print("\n" + "=" * 60)
        print("🚀 UDAAN X AI")
        print(TAGLINE)
        print("=" * 60)

        print("👑 Founder Authority : ACTIVE")
        print("🧠 AI Brain         :", "CONNECTED"
              if self.brain.api_key else "NOT CONFIGURED")
        print("🤖 AI Agents        :", len(self.team))

        print("\nAI TEAM:")

        for number, agent in enumerate(
            self.team.values(), 1
        ):
            print(
                f"{number}. {agent.name} → {agent.role}"
            )

        print("\nType 'exit' to close.")

        while True:

            command = input("\n👑 Founder > ").strip()

            if command.lower() == "exit":
                print("\nUDAAN X safely stopped.")
                break

            if not command:
                continue

            self.execute(command)


if __name__ == "__main__":

    app = UdaanX()
    app.start()