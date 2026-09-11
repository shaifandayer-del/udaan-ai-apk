# ==========================================
# UDAAN AI - DEVELOPER EXECUTOR
# STEP 113
# ==========================================

import os
import subprocess
from datetime import datetime


class DeveloperExecutor:

    def __init__(self):

        self.base_directory = os.path.abspath(
            "udaan_projects"
        )

    def get_timestamp(self):

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def prepare_project(self, project_name):

        project_name = str(
            project_name or
            "UDAAN Generated Project"
        ).strip()

        safe_name = "".join(
            character
            if character.isalnum()
            or character in ("-", "_")
            else "_"
            for character in project_name
        )

        project_path = os.path.join(
            self.base_directory,
            safe_name
        )

        os.makedirs(
            project_path,
            exist_ok=True
        )

        return project_path

    def run_command(
        self,
        command,
        working_directory=None
    ):

        try:

            process = subprocess.run(
                command,
                shell=True,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=120
            )

            return {
                "status": (
                    "SUCCESS"
                    if process.returncode == 0
                    else "FAILED"
                ),
                "return_code":
                    process.returncode,
                "stdout":
                    process.stdout[-5000:],
                "stderr":
                    process.stderr[-5000:]
            }

        except subprocess.TimeoutExpired:

            return {
                "status": "FAILED",
                "message":
                    "Developer command timeout ho gaya."
            }

        except Exception as error:

            return {
                "status": "FAILED",
                "message":
                    "Developer execution failed.",
                "error":
                    str(error)
            }

    def execute_build(
        self,
        project_name,
        build_command=None
    ):

        timestamp = self.get_timestamp()

        project_path = self.prepare_project(
            project_name
        )

        result = {
            "status": "READY",
            "agent": "Developer AI",
            "project_name": project_name,
            "project_path": project_path,
            "created_at": timestamp
        }

        if build_command:

            build_result = self.run_command(
                build_command,
                project_path
            )

            result["build"] = build_result

            if build_result.get("status") == "FAILED":

                result["status"] = "FAILED"

            else:

                result["status"] = "SUCCESS"

        return result


_executor = DeveloperExecutor()


def execute_build(
    project_name,
    build_command=None
):

    return _executor.execute_build(
        project_name,
        build_command
    )


if __name__ == "__main__":

    result = execute_build(
        "UDAAN Test Project"
    )

    print()
    print("================================")
    print("     DEVELOPER EXECUTOR")
    print("================================")
    print()
    print(result)
