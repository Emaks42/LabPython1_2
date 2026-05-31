import random

from src.task_working.task import Task
import asyncio


class UnstableHandlerError(Exception):
    ...


class UnstableHandler:
    def __init__(self):
        self.params = {"delay": 0.2}

    async def handle_task(self, task: dict):
        task_ = Task.from_dict(task)
        if task_.priority is not None:
            if random.randint(1, task_.priority) == 1:
                await asyncio.sleep(task_.priority * self.params["delay"])
            else:
                raise UnstableHandlerError(f"{task_}")
        else:
            raise UnstableHandlerError(f"{task_}")

    def get_params(self):
        return self.params
