# YouTubeOAuth.py

import os


CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_UPLOAD_SCOPE = (
    "https://www.googleapis.com/auth/youtube.upload"
)


def check_oauth_files():

    result = {
        "status": "NOT_READY",
        "client_secrets": False,
        "oauth_scope": YOUTUBE_UPLOAD_SCOPE
    }

    if os.path.exists(CLIENT_SECRETS_FILE):

        result["client_secrets"] = True
        result["status"] = "CONFIGURED"

    return result


def get_oauth_status():

    return check_oauth_files()


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — YOUTUBE OAUTH CHECK")
    print("=" * 60)

    result = get_oauth_status()

    print()
    print("🔐 OAuth Scope:")
    print(result["oauth_scope"])

    print()
    print(
        "📄 client_secrets.json:",
        "FOUND"
        if result["client_secrets"]
        else "NOT FOUND"
    )

    print()
    print("📊 Status:", result["status"])

    if result["status"] == "CONFIGURED":

        print()
        print("🟢 OAuth configuration detected.")

    else:

        print()
        print(
            "🟡 OAuth setup pending."
        )

        print(
            "Real YouTube login/upload "
            "abhi enabled nahi hai."
        )

    print()
    print("=" * 60)
    print("✅ YOUTUBE OAUTH CHECK COMPLETE")
    print("=" * 60)