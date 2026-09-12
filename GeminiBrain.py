import os
import urllib.request
import urllib.error
import json

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"

def ask_gemini(command):
    if not API_KEY:
        return {
            "status": "FAILED",
            "message": "GEMINI_API_KEY not configured."
        }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{MODEL}:generateContent?key={API_KEY}"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are UDAAN AI, the founder's personal "
                            "AI Command Center. Understand Hindi, Hinglish "
                            "and English. Give clear, useful answers.\n\n"
                            f"Founder Command:\n{command}"
                        )
                    }
                ]
            }
        ]
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        return {
            "status": "SUCCESS",
            "message": answer,
            "model": MODEL
        }

    except urllib.error.HTTPError as error:
        return {
            "status": "FAILED",
            "message": "Gemini API error.",
            "error": error.read().decode("utf-8")
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "message": "Gemini connection error.",
            "error": f"{type(error).__name__}: {error}"
        }

def run(command=""):
    return ask_gemini(command)

def execute(command=""):
    return ask_gemini(command)

def process(command=""):
    return ask_gemini(command)

def handle(command=""):
    return ask_gemini(command)

def run_agent(command=""):
    return ask_gemini(command)
