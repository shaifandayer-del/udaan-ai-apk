import json
import urllib.request
import urllib.error


BASE_URL = "http://127.0.0.1:8080"


def get_request(path):

    url = BASE_URL + path

    try:

        with urllib.request.urlopen(
            url,
            timeout=5
        ) as response:

            data = response.read().decode("utf-8")

            return {
                "success": True,
                "status_code": response.status,
                "data": json.loads(data)
            }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


def post_command(command):

    url = BASE_URL + "/command"

    payload = json.dumps({
        "command": command
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:

            data = response.read().decode("utf-8")

            return {
                "success": True,
                "status_code": response.status,
                "data": json.loads(data)
            }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("          UDAAN AI — API LIVE TEST")
    print("=" * 60)

    print()
    print("🌐 Testing GET /status")

    status = get_request("/status")

    print(status)

    print()
    print("🧠 Testing POST /command")

    result = post_command(
        "research latest AI trends"
    )

    print(result)

    print()
    print("=" * 60)

    if status["success"] and result["success"]:

        print("✅ API LIVE TEST PASSED")

    else:

        print("❌ API LIVE TEST FAILED")

    print("=" * 60)