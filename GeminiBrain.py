# ==========================================
# UDAAN AI - GEMINI BRAIN
# STEP 5
# ==========================================

import urllib.request
import urllib.error
import json


# Apni Gemini API key yahan paste karo
API_KEY = "YAHAN_APNI_GEMINI_API_KEY_DALO"


MODEL = "gemini-2.5-flash"


def ask_gemini(command):

    if not API_KEY or API_KEY == "YAHAN_APNI_GEMINI_API_KEY_DALO":
        return "udaan ai."

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/"
        + MODEL
        + ":generateContent?key="
        + API_KEY
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are the Main AI of Udaan AI. "
                            "Answer the founder clearly and helpfully. "
                            "The founder may use Hindi or English.\n\n"
                            "Founder Command:\n"
                            + command
                        )
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
            timeout=30
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        return answer

    except urllib.error.HTTPError as error:

        print("❌ GEMINI API ERROR")
        print("HTTP:", error.code)

        try:
            print(error.read().decode("utf-8"))
        except Exception:
            pass

        return "Gemini API error."

    except Exception as error:

        print("❌ CONNECTION ERROR")
        print(error)

        return "Gemini connection error."


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("================================")
    print("       UDAAN AI")
    print("      GEMINI BRAIN")
    print("================================")
    print()

    answer = ask_gemini(
        "Udaan AI ke liye ek short welcome message likho."
    )

    print("🧠 GEMINI RESPONSE:")
    print()
    print(answer)