from src.task_sources.protocol_source import TaskSource
from src.task_working.task import Task
from typing import Generator, Dict, Type, Any, Iterable
from copy import deepcopy


class TaskIterator:
    gen: Generator
    prior_filter: int | None = None
    status_filter: int | None = None

    def __init__(self, sources: list[TaskSource], order: list[int], task_list: list[Task] | None = None):
        def gen():
            tasks = deepcopy(task_list) or []
            ended_sources = [0] * len(sources)
            pos = 0
            while sum(ended_sources) != len(sources):
                if len(tasks) != 0:
                    new_task = tasks.pop(0)
                else:
                    new_task = Task.from_dict(sources[order[pos]].get_task())
                    if sources[order[pos]].is_tasks_ended():
                        ended_sources[order[pos]] = 1
                    pos = (pos + 1) % len(order)
                    while ended_sources[order[pos]] and sum(ended_sources) != len(sources):
                        pos = (pos + 1) % len(order)
                yield new_task
        self.gen = gen()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.gen)


class TaskQueue:
    sources: list[tuple[Type, Dict[str, Any]]]
    order: list[int]
    tasks: list[Task]

    def __init__(self, sources: list[tuple[Type, Dict[str, Any]]], order: list[int]):
        for source in sources:
            if not isinstance(source[0], TaskSource):
                raise ValueError("нельзя передавать в очередь задач не объекты, " +\
                                 "не реализующие контракт источника задач")
        self.sources = sources
        self.order = order
        self.tasks = list()

    def __iter__(self) -> TaskIterator:
        sources = []
        for source in self.sources:
            sources.append(source[0](**source[1]))
        return TaskIterator(sources, self.order, self.tasks)

    def push(self, task: Task):
        if not isinstance(task, Task):
            raise ValueError("В очередь задач можно добавлять только задачи (класс Task)")
        self.tasks.append(task)

    def push_task_list(self, task_list: list[Task]):
        if not isinstance(task_list, Iterable):
            raise ValueError("передан не итерируемый объект")
        for task in task_list:
            self.push(task)

    def pop(self):
        return self.tasks.pop(0)

    def get_generator(self) -> Generator[Task]:
        added_tasks = deepcopy(self.tasks) or []
        ended_sources = [0] * len(self.sources)
        sources = [source[0](**source[1]) for source in self.sources]
        pos = 0
        while sum(ended_sources) != len(self.sources):
            if len(added_tasks) != 0:
                new_task = added_tasks.pop(0)
            else:
                new_task = Task.from_dict(sources[self.order[pos]].get_task())
                if sources[self.order[pos]].is_tasks_ended():
                    ended_sources[self.order[pos]] = 1
                pos = (pos + 1) % len(self.order)
                while ended_sources[self.order[pos]] and sum(ended_sources) != len(sources):
                    pos = (pos + 1) % len(self.order)
            pushed_tasks = yield new_task
            if pushed_tasks is not None:
                if isinstance(pushed_tasks, Iterable):
                    added_tasks.extend(pushed_tasks)
                else:
                    added_tasks.append(pushed_tasks)
