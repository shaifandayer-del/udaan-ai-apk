# ==========================================
# UDAAN AI - DEVELOPER AI
# STEP 94
# ==========================================

import datetime
import re


APP_KEYWORDS = [
    "app banao",
    "app bana",
    "application banao",
    "android app",
    "software banao",
    "software bana",
    "website banao",
    "project banao",
    "build app",
    "build software",
    "create app",
    "create software",
    "develop app",
    "develop software",
]

CODE_KEYWORDS = [
    "code",
    "coding",
    "python",
    "kotlin",
    "java",
    "android",
    "program",
    "developer",
    "bug",
    "fix",
    "debug",
]


def get_timestamp():
    return datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def detect_task_type(command):
    """
    Developer command ka type detect karta hai.
    """

    text = command.lower().strip()

    for keyword in APP_KEYWORDS:
        if keyword in text:
            return "app_build"

    for keyword in CODE_KEYWORDS:
        if keyword in text:
            return "software_development"

    return "software_development"


def extract_project_name(command):
    """
    Basic project/app name detection.
    """

    text = command.strip()

    patterns = [
        r"app banao\s+(.+)",
        r"app bana\s+(.+)",
        r"create app\s+(.+)",
        r"build app\s+(.+)",
        r"software banao\s+(.+)",
        r"website banao\s+(.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            if name:
                return name[:100]

    return "UDAAN Generated Project"


def build_project_plan(command):
    """
    App/software build ke liye structured plan.
    """

    project_name = extract_project_name(command)

    return {
        "project_name": project_name,
        "requirements": [
            "Understand Founder requirements",
            "Create project structure",
            "Generate required source files",
            "Configure dependencies",
            "Run syntax/build checks",
            "Run tests",
            "Prepare final build"
        ],
        "workflow": [
            "REQUIREMENTS",
            "ARCHITECTURE",
            "CODE_GENERATION",
            "BUILD",
            "TEST",
            "FOUNDER_REVIEW",
            "FINAL_BUILD"
        ]
    }


def requires_founder_approval(task_type):
    """
    Real build/publish type actions ke liye
    Founder approval mandatory rahega.
    """

    protected_tasks = [
        "app_build",
        "software_development"
    ]

    return task_type in protected_tasks


def developer_task(command):

    timestamp = get_timestamp()

    command = str(command).strip()

    print()
    print("================================")
    print("        UDAAN DEVELOPER AI")
    print("================================")
    print()

    if not command:

        return {
            "status": "FAILED",
            "agent": "Developer AI",
            "message": "Developer command empty hai.",
            "created_at": timestamp
        }

    task_type = detect_task_type(command)

    print("💻 Developer Command:")
    print(command)
    print()

    if task_type == "app_build":

        project_plan = build_project_plan(
            command
        )

        result = {
            "status": "READY_FOR_APPROVAL",
            "agent": "Developer AI",
            "command": command,
            "created_at": timestamp,
            "task_type": task_type,
            "project": project_plan,
            "founder_approval_required": True,
            "message": (
                "App/software build request prepared. "
                "Founder approval required before execution."
            )
        }

    else:

        result = {
            "status": "SUCCESS",
            "agent": "Developer AI",
            "command": command,
            "created_at": timestamp,
            "task_type": task_type,
            "founder_approval_required": False,
            "message": (
                "Developer task received and prepared."
            )
        }

    print("✅ DEVELOPER AI READY")
    print()

    return result


def run(command):
    return developer_task(command)


def execute(command):
    return developer_task(command)


def process(command):
    return developer_task(command)


def handle(command):
    return developer_task(command)


if __name__ == "__main__":

    command = input(
        "💻 Developer command: "
    ).strip()

    result = developer_task(command)

    print()
    print("🧠 DEVELOPER RESULT")
    print(result)
