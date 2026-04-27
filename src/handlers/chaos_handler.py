import asyncio
import random


class ChaosHandler:
    def __init__(self, params: dict | None = None):
        self.params = params or {"chaotic": True}

    async def handle_task(self, task: dict):
        random.seed(self.params.get("seed") or random.random())
        await asyncio.sleep((task.get("priority") or 1) * random.uniform(self.params.get("limits", [0])[0],
                                                                         self.params.get("limits", [0, 1])[1]))

    def get_params(self):
        return self.params
