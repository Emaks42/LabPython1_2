from src.task_working.task import Task
import asyncio


class PrintHandler:
    def __init__(self):
        self.params = {"delay": 0.2}

    async def handle_task(self, task: dict):
        task_ = Task.from_dict(task)
        if task_.priority is not None:
            print(task_.priority * self.params["delay"])
            await asyncio.sleep(task_.priority * self.params["delay"])
        else:
            print(self.params["delay"])
            await asyncio.sleep(self.params["delay"])
        print("proceed", task_)

    def get_params(self):
        return self.params
