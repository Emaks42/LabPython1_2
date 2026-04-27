import random


class RandomDistributor:
    def __init__(self, seed: int | None = None):
        if seed:
            random.seed(seed)
        self.seed = random.random()

    def does_task_fit(self, task: dict, worker_params: dict) -> bool:
        random.seed(self.seed)
        res = random.randint(1, int(task.get(id, 5) + worker_params.get("delay", 0.1) * 100) % 3 + 2) == 1
        self.seed = random.random()
        return res
