from core.automation.logger import log_event
from core.automation.task_manager import TaskManager


class AutomationRunner:
    def __init__(self):
        self.tasks = TaskManager()

    def run(self, name, action):
        task_id = self.tasks.create_task(name)
        log_event("TASK_CREATED", f"id={task_id} name={name}")

        self.tasks.update_status(task_id, "running")
        log_event("TASK_RUNNING", f"id={task_id}")

        try:
            result = action()

            self.tasks.update_status(task_id, "completed")
            log_event("TASK_COMPLETED", f"id={task_id}")

            return {
                "success": True,
                "task_id": task_id,
                "result": result
            }

        except Exception as error:
            self.tasks.update_status(task_id, "failed")
            log_event("TASK_FAILED", f"id={task_id} error={error}")

            return {
                "success": False,
                "task_id": task_id,
                "error": str(error)
            }
