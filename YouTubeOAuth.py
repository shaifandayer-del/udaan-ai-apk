import os
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]

TOKEN_FILE = Path("youtube_token.json")


def get_client_config():
    client_json = os.getenv("YOUTUBE_CLIENT_JSON", "")

    if not client_json:
        return None

    try:
        return json.loads(client_json)
    except json.JSONDecodeError:
        return None


def load_credentials():
    token_json = os.getenv("YOUTUBE_TOKEN_JSON", "")

    if token_json:
        try:
            return Credentials.from_authorized_user_info(
                json.loads(token_json),
                SCOPES
            )
        except Exception:
            pass

    if TOKEN_FILE.exists():
        try:
            return Credentials.from_authorized_user_file(
                str(TOKEN_FILE),
                SCOPES
            )
        except Exception:
            pass

    return None


def save_credentials(credentials):
    token_data = credentials.to_json()

    os.environ["YOUTUBE_TOKEN_JSON"] = token_data

    try:
        TOKEN_FILE.write_text(
            token_data,
            encoding="utf-8"
        )
    except Exception:
        pass

    return {
        "status": "SUCCESS",
        "message": "YouTube OAuth credentials saved."
    }


def create_authorization_url():
    client_config = get_client_config()

    if client_config is None:
        return {
            "status": "FAILED",
            "message": "YOUTUBE_CLIENT_JSON configured nahi hai."
        }

    try:
        flow = InstalledAppFlow.from_client_config(
            client_config,
            SCOPES
        )

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            prompt="consent",
            include_granted_scopes="true"
        )

        return {
            "status": "SUCCESS",
            "authorization_url": authorization_url,
            "state": state
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "message": "YouTube OAuth URL create nahi hua.",
            "error": f"{type(error).__name__}: {error}"
        }


def authenticate():
    client_config = get_client_config()

    if client_config is None:
        return {
            "status": "FAILED",
            "message": "YOUTUBE_CLIENT_JSON configured nahi hai."
        }

    try:
        flow = InstalledAppFlow.from_client_config(
            client_config,
            SCOPES
        )

        credentials = flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent"
        )

        save_credentials(credentials)

        return {
            "status": "SUCCESS",
            "connected": True,
            "message": "YouTube OAuth authentication successful."
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "connected": False,
            "message": "YouTube OAuth authentication failed.",
            "error": f"{type(error).__name__}: {error}"
        }


def check_connection():
    credentials = load_credentials()

    if credentials is None:
        return {
            "status": "
