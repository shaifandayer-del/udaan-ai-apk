
import datetime
import uuid


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, command, agent="Main AI"):
        command = str(command or "").strip()
        agent = str(agent or "Main AI").strip()

        if not command:
            return {
                "status": "FAILED",
                "message": "Task command is empty."
            }

        task_id = str(uuid.uuid4())

        task = {
            "task_id": task_id,
            "command": command,
            "agent": agent,
            "status": "PENDING",
            "created_at": datetime.datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None
        }

        self.tasks[task_id] = task
        return task

    def start_task(self, task_id):
        task = self.tasks.get(str(task_id))

        if not task:
            return {
                "status": "FAILED",
                "message": "Task not found."
            }

        task["status"] = "IN_PROGRESS"
        task["started_at"] = datetime.datetime.now().isoformat()

        return task

    def complete_task(self, task_id, result=None):
        task = self.tasks.get(str(task_id))

        if not task:
            return {
                "status": "FAILED",
                "message": "Task not found."
            }

        task["status"] = "DONE"
        task["completed_at"] = datetime.datetime.now().isoformat()
        task["result"] = result

        return task

    def fail_task(self, task_id, error):
        task = self.tasks.get(str(task_id))

        if not task:
            return {
                "status": "FAILED",
                "message": "Task not found."
            }

        task["status"] = "FAILED"
        task["completed_at"] = datetime.datetime.now().isoformat()
        task["error"] = str(error)

        return task

    def get_task(self, task_id):
        return self.tasks.get(str(task_id))

    def get_all_tasks(self):
        return list(self.tasks.values())

    def get_tasks_by_status(self, status):
        status = str(status or "").strip().upper()

        return [
            task
            for task in self.tasks.values()
            if task["status"].upper() == status
        ]

    def delete_task(self, task_id):
        task_id = str(task_id)

        if task_id not in self.tasks:
            return {
                "status": "FAILED",
                "message": "Task not found."
            }

        del self.tasks[task_id]

        return {
            "status": "SUCCESS",
            "task_id": task_id,
            "message": "Task deleted."
        }


task_manager = TaskManager()


def create_task(command, agent="Main AI"):
    return task_manager.create_task(command, agent)


def start_task(task_id):
    return task_manager.start_task(task_id)


def complete_task(task_id, result=None):
    return task_manager.complete_task(task_id, result)


def fail_task(task_id, error):
    return task_manager.fail_task(task_id, error)


def get_task(task_id):
    return task_manager.get_task(task_id)


def get_all_tasks():
    return task_manager.get_all_tasks()


def get_tasks_by_status(status):
    return task_manager.get_tasks_by_status(status)


def delete_task(task_id):
    return task_manager.delete_task(task_id)
