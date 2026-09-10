# UdaanAPI.py
# Udaan AI - Local API Server

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from UdaanCommandCenter import (
    execute_command,
    get_command_center_status
)


HOST = "127.0.0.1"
PORT = 8080


def api_status():
    """
    Compatibility status function
    used by PythonFunctionalTest and other modules.
    """

    try:
        center_status = get_command_center_status()
    except Exception as error:
        center_status = {
            "status": "ERROR",
            "error": str(error)
        }

    return {
        "app": "Udaan AI",
        "module": "UdaanAPI",
        "status": "ONLINE",
        "host": HOST,
        "port": PORT,
        "command_center": center_status
    }


def handle_command(command):
    """
    Compatibility command function.
    Sends command directly to Udaan Command Center.
    """

    if not command:
        return {
            "status": "FAILED",
            "message": "Command is empty."
        }

    try:

        result = execute_command(command)

        return {
            "status": "SUCCESS",
            "command": command,
            "result": result
        }

    except Exception as error:

        return {
            "status": "FAILED",
            "command": command,
            "error": str(error)
        }


class UdaanAPIHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):

        body = json.dumps(
            data,
            ensure_ascii=False,
            default=str
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):

        if self.path == "/":

            self.send_json({
                "name": "Udaan AI API",
                "status": "ONLINE",
                "service": "Command Center"
            })

            return

        if self.path == "/status":

            self.send_json(
                api_status()
            )

            return

        self.send_json(
            {
                "error": "Endpoint not found"
            },
            404
        )

    def do_POST(self):

        if self.path != "/command":

            self.send_json(
                {
                    "error": "Endpoint not found"
                },
                404
            )

            return

        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            raw_data = self.rfile.read(
                content_length
            )

            data = json.loads(
                raw_data.decode("utf-8")
            )

            command = data.get(
                "command",
                ""
            )

            result = handle_command(
                command
            )

            self.send_json(result)

        except Exception as error:

            self.send_json(
                {
                    "status": "FAILED",
                    "message": "API request failed.",
                    "error": str(error)
                },
                500
            )

    def log_message(self, format, *args):

        print(
            "🌐 API:",
            format % args
        )


def start_server():

    server = HTTPServer(
        (HOST, PORT),
        UdaanAPIHandler
    )

    print()
    print("=" * 60)
    print("             UDAAN AI API SERVER")
    print("=" * 60)

    print()
    print("🟢 Server :", "ONLINE")
    print("📡 Host   :", HOST)
    print("🔌 Port   :", PORT)

    print()
    print("Endpoints:")
    print("GET  /")
    print("GET  /status")
    print("POST /command")

    print()
    print("Press CTRL+C to stop.")
    print("=" * 60)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print()
        print("🛑 Server stopping...")

    finally:

        server.server_close()


if __name__ == "__main__":

    start_server()