from time import perf_counter_ns, sleep
from src.constants import API_ANSWERS
from random import randint
from hashlib import sha256
import asyncio


class APISource:
    """
    Источник задач - API-заглушка
    :cvar time - время начала "приёма" данных
    :cvar timeout - задержка (формируется из адреса)
    """
    time: int
    timeout: int

    def __init__(self, address: str = "base"):
        self.timeout = int((sha256(address.encode())).hexdigest()[:3], 16)
        self.time = perf_counter_ns()

    def get_task(self) -> dict:
        sleep(0.00001 * randint(1, 3) * self.timeout)
        return API_ANSWERS[(perf_counter_ns() - self.time) % len(API_ANSWERS)]

    def is_tasks_ended(self) -> bool:
        return not bool((perf_counter_ns() - self.time) % 20)

    async def get_task_async(self) -> dict:
        await asyncio.sleep(0.00001 * randint(1, 3) * self.timeout)
        return API_ANSWERS[(perf_counter_ns() - self.time) % len(API_ANSWERS)]
