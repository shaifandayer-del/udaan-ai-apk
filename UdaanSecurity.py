UdaanSecurity.py

import hashlib
import hmac
import os
import secrets


class UdaanSecurity:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv(
            "UDAAN_FOUNDER_API_KEY",
            ""
        )

    def is_configured(self):
        return bool(self.api_key)

    def verify_api_key(self, provided_key):
        if not self.api_key or not provided_key:
            return False

        return hmac.compare_digest(
            self.api_key,
            str(provided_key)
        )

    def generate_token(self, length=32):
        return secrets.token_urlsafe(length)

    def hash_value(self, value):
        return hashlib.sha256(
            str(value).encode("utf-8")
        ).hexdigest()

    def verify_hash(self, value, expected_hash):
        actual_hash = self.hash_value(value)

        return hmac.compare_digest(
            actual_hash,
            str(expected_hash)
        )

    def sanitize_command(self, command):
        if command is None:
            return ""

        command = str(command).strip()

        if len(command) > 5000:
            command = command[:5000]

        return command

    def security_status(self):
        return {
            "api_key_configured": self.is_configured(),
            "authentication": "ENABLED"
            if self.is_configured()
            else "DISABLED"
        }


security = UdaanSecurity()


def verify_api_key(provided_key):
    return security.verify_api_key(provided_key)


def sanitize_command(command):
    return security.sanitize_command(command)


def security_status():
    return security.security_status()
