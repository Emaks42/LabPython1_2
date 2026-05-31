from src.task_working.task import Task
import asyncio


class PrintHandler:
    def __init__(self):
        self.params = {"delay": 0.2}

    async def handle_task(self, task: dict):
        task_ = Task.from_dict(task)
        print(type(task_.priority), type(self.params["delay"]))
        if task_.priority is not None:
            await asyncio.sleep(task_.priority * self.params["delay"])
        else:
            print("beep")
            await asyncio.sleep(self.params["delay"])
        print("processed", task_)

    def get_params(self):
        return self.params
