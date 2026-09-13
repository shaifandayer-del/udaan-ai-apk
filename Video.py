Video.py

import os
import datetime


def create_video(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Video AI",
            "message": "Video command is empty."
        }

    try:
        from VideoProductionPipeline import create_video_project

        result = create_video_project(command)

        if isinstance(result, dict):
            if result.get("status") == "SUCCESS":
                return result

            return {
                "status": "FAILED",
                "agent": "Video AI",
                "message": result.get(
                    "message",
                    "Video production failed."
                ),
                "details": result
            }

        if result:
            return {
                "status": "SUCCESS",
                "agent": "Video AI",
                "message": "Video project created successfully.",
                "result": result
            }

    except Exception as error:
        print("VideoProductionPipeline error:", error)

    try:
        from ActualVideoRenderer import render_video

        output = render_video(command)

        if output:
            if os.path.exists(str(output)):
                return {
                    "status": "SUCCESS",
                    "agent": "Video AI",
                    "message": "Video rendered successfully.",
                    "output_file": str(output),
                    "created_at": datetime.datetime.now().isoformat()
                }

    except Exception as error:
        print("ActualVideoRenderer error:", error)

    return {
        "status": "FAILED",
        "agent": "Video AI",
        "message": "Video could not be generated."
    }


def video(command):
    return create_video(command)


def run(command):
    return create_video(command)


def execute(command):
    return create_video(command)


def process(command):
    return create_video(command)


def handle(command):
    return create_video(command)


if __name__ == "__main__":
    command = input("Video command: ")
    print(create_video(command))
