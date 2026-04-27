import logging

from src.task_sources.protocol_source import TaskSource
from src.task_working.task import Task
from src.constants import PRIORITY_LIMITATIONS, POSSIBLE_STATUSES
from src.task_working.task_queue import ValidatedField, TaskQueueError
import asyncio
import random


class AsyncTaskQueue:
    """
    Асинхронная очередь задач, подерживающая итерацию и получение информации из источников и ленивые фильтры
    :cvar sources - набор источников задач
    :cvar order - порядок обращения к источникам
    :cvar tasks - список задач
    """
    sources: list[TaskSource]
    order: list[int]
    tasks: asyncio.Queue[Task | None]
    prior_filter = ValidatedField(PRIORITY_LIMITATIONS, int, "prior_filter")
    status_filter = ValidatedField(POSSIBLE_STATUSES, str, "status_filter")

    def __init__(self, maxsize: int = 3, sources: list[TaskSource] | None = None,
                 order: list[int] | None = None, prior_filter: int | None = None, status_filter: int | None = None):
        if sources is not None:
            for source in sources:
                if not isinstance(source, TaskSource):
                    raise TaskQueueError("нельзя передавать в очередь задач не объекты, " +
                                         "не реализующие контракт источника задач")
        if sources is None:
            sources = []
        self.sources = sources
        if order is not None:
            if any(ord_ >= len(sources) for ord_ in order):
                raise TaskQueueError("некорректный порядок обхода источников, индекс источника выходит"
                                     " за границы массива")
        if order is None:
            order = list(range(len(sources)))
        self.order = order
        self.tasks = asyncio.Queue()
        self.status_filter = status_filter
        self.prior_filter = prior_filter
        self.seed = random.random()
        self.ended_sources = [0] * len(self.sources)
        self.pos = 0

    async def push(self, task: Task | None):
        if not isinstance(task, Task) and task is not None:
            raise TaskQueueError("В очередь задач можно добавлять только задачи (класс Task)")
        await self.tasks.put(task)
        print("added", task)

    async def pop(self):
        while sum(self.ended_sources) != len(self.sources) or not self.tasks.empty():
            if not self.tasks.empty():
                res = await self.tasks.get()
                return res
            else:
                logging.info("blob")
                new_task = Task.from_dict(await self.sources[self.order[self.pos]].get_task_async())
                if self.sources[self.order[self.pos]].is_tasks_ended():
                    self.ended_sources[self.order[self.pos]] = 1
                self.pos = (self.pos + 1) % len(self.order)
                while self.ended_sources[self.order[self.pos]] and sum(self.ended_sources) != len(self.sources):
                    self.pos = (self.pos + 1) % len(self.order)
            await self.tasks.put(new_task)

    async def join(self):
        while sum(self.ended_sources) != len(self.sources):
            await self.tasks.join()

    def immediate_push(self, task: Task):
        if not isinstance(task, Task) and task is not None:
            raise TaskQueueError("В очередь задач можно добавлять только задачи (класс Task)")
        self.tasks.put_nowait(task)
        print("added", task)
