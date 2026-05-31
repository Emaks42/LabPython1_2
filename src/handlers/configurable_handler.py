from src.task_working.task import Task
import asyncio
from src.constants import PRIORITY_LIMITATIONS


class ConfigurableHandler:
    base_delay = 0.2

    def __init__(self, params: dict | None = None):
        self.params = params or {"delay": self.base_delay}
        self.params["delay"] = self.base_delay

    async def handle_task(self, task: dict):
        task_ = Task.from_dict(task)
        if task_.priority is not None:
            if self.params.get("reverse_priority"):
                task_.priority = PRIORITY_LIMITATIONS[1] - task_.priority
            await asyncio.sleep(task_.priority * self.params["delay"] * (self.params.get("priority_scaling") or 1))
        else:
            await asyncio.sleep(self.params["delay"] * (self.params.get("priority_scaling") or 1))

    def get_params(self):
        return self.params
