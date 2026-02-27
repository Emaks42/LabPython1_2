from time import perf_counter_ns, sleep
from src.constants import API_ANSWERS
from random import randint
from hashlib import sha256


class APISource:
    time: int
    timeout: int

    def __init__(self, address: str = "base"):
        self.timeout = int((sha256(address.encode())).hexdigest()[:3], 16)
        self.time = perf_counter_ns()

    def get_task(self) -> str:
        sleep(0.00001 * randint(1, 3) * self.timeout)
        return API_ANSWERS[(perf_counter_ns() - self.time) % len(API_ANSWERS)]

    def is_tasks_ended(self) -> bool:
        return not bool((perf_counter_ns() - self.time) % 20)
