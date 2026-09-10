import json
import urllib.request
import urllib.error

API_URL = "http://127.0.0.1:8080"

# IMPORTANT:
# Is value ko UdaanSecurity.py ke API_KEY
# ke EXACT same value se replace karo.
API_KEY = "UDAAN_FOUNDER_CHANGE_THIS_KEY"


def test_health():
    print()
    print("🔎 Testing API Health...")

    try:
        request = urllib.request.Request(
            API_URL + "/health",
            method="GET"
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8")

        print("✅ Health API working")
        print(data)

    except Exception as error:
        print("❌ Health test failed")
        print(error)


def test_command():
    print()
    print("🧠 Testing Secure Command API...")

    payload = {
        "command": "Research AI ko Udaan AI ke liye ek topic research karne do"
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        API_URL + "/command",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Udaan-Key": API_KEY
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = response.read().decode("utf-8")

        print("✅ Secure command accepted")
        print(result)

    except urllib.error.HTTPError as error:

        print("❌ API rejected request")
        print("HTTP:", error.code)

        try:
            print(error.read().decode("utf-8"))
        except Exception:
            pass

    except Exception as error:

        print("❌ Connection failed")
        print(error)


if __name__ == "__main__":

    print("================================")
    print("       UDAAN AI API TEST")
    print("================================")

    test_health()
    test_command()