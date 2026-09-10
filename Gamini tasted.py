import urllib.request
import urllib.error
import json

API_KEY = "YAHAN_APNI_GEMINI_API_KEY_DALO"

def test_gemini():

    if API_KEY == "YAHAN_APNI_GEMINI_API_KEY_DALO":
        print("udaan ai")
        return

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent?key="
        + API_KEY
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say exactly: UDAAN X AI CONNECTED"
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
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = result["candidates"][0]["content"]["parts"][0]["text"]

        print("✅ GEMINI CONNECTION SUCCESS")
        print(answer)

    except urllib.error.HTTPError as error:
        print("❌ GEMINI API ERROR")
        print("HTTP:", error.code)

        try:
            print(error.read().decode("utf-8"))
        except Exception:
            pass

    except Exception as error:
        print("❌ CONNECTION ERROR")
        print(error)


if __name__ == "__main__":
    test_gemini()