import random
from hashlib import sha256
from constants import TASK_PURPOSES, TASK_DESTINATIONS


class GeneratorSource:
    state: object
    chance_of_eof: int

    def __init__(self, seed: int = random.randint(1, 100), amount_of_tasks: int = random.randint(10, 100)):
        random.seed(seed)
        self.state = random.getstate()
        self.amount_of_tasks = amount_of_tasks
        self.returned_tasks_count = 0

    def get_task(self) -> str:
        random.setstate(self.state)
        destinantions_amount = random.randint(1, 2)
        task = random.choice(TASK_PURPOSES)
        for i in range(destinantions_amount):
            task += " " + random.choice(TASK_DESTINATIONS)
        self.state = random.getstate()
        task = str(int((sha256(task.encode())).hexdigest()[:3], 16)) + " - " + task
        self.returned_tasks_count += 1
        return task

    def is_tasks_ended(self) -> bool:
        return self.returned_tasks_count >= self.amount_of_tasks
