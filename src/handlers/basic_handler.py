from src.task_working.task import Task
import asyncio


class BasicHandler:
    def __init__(self):
        self.params = {"delay": 0.01}

    async def handle_task(self, task: dict):
        task_ = Task.from_dict(task)
        if task_.priority is not None:
            print(task_.priority * self.params["delay"])
            timeout = task_.priority * self.params["delay"]
            await asyncio.wait_for(asyncio.sleep(timeout), timeout=timeout)
            print("slept")
        else:
            print(self.params["delay"])
            timeout = self.params["delay"]
            await asyncio.wait_for(asyncio.sleep(timeout), timeout=timeout)
            print("slept")
        return

    def get_params(self):
        return self.params
