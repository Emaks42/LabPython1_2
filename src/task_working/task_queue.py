from src.task_sources.protocol_source import TaskSource
from src.task_working.task import Task
from typing import Generator, Dict, Type, Any, Iterable
from copy import deepcopy
from src.constants import PRIORITY_LIMITATIONS, POSSIBLE_STATUSES


class TaskQueueError(Exception):
    ...


class ValidatedField:
    def __init__(self, lim, type_, name, err_type: Type = TaskQueueError):
        self.limitations = lim
        self.type = type_
        self.name = "__" + name
        self.err_type = err_type

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, val):
        all_skip = False
        if not isinstance(val, self.type):
            if isinstance(val, str):
                val = self.type(val.strip())
            elif val is not None:
                raise self.err_type(f"значение {self.name[2:]} должно быть {self.type}")
            if val is None:
                all_skip = True
        if isinstance(self.limitations, tuple) and not all_skip:
            if not (self.limitations[0] < val < self.limitations[1]):
                raise self.err_type(
                    f"значение {self.name[2:]} должно быть в диапазоне от {self.limitations[0]} до " +
                    f"{self.limitations[1]}")
        elif isinstance(self.limitations, list) and not all_skip:
            if val not in self.limitations:
                raise self.err_type(f"значение {self.name[2:]} должно быть в диапазоне {self.limitations}")
        instance.__dict__[self.name] = val


class TaskIterator:
    gen: Generator

    def __init__(self, sources: list[TaskSource], order: list[int], task_list: list[Task] | None = None,
                 prior_filter: int | None = None, status_filter: int | None = None):
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
                if prior_filter is not None:
                    if new_task.priority != prior_filter:
                        continue
                if status_filter is not None:
                    if new_task.status != status_filter:
                        continue
                yield new_task
        self.gen = gen()

    def __iter__(self):
        return self

    def __next__(self) -> Task | None:
        return next(self.gen)


class TaskQueue:
    sources: list[tuple[Type, Dict[str, Any]]]
    order: list[int]
    tasks: list[Task]
    prior_filter = ValidatedField(PRIORITY_LIMITATIONS, int, "prior_filter")
    status_filter = ValidatedField(POSSIBLE_STATUSES, str, "status_filter")

    def __init__(self, sources: list[tuple[Type, Dict[str, Any]]], order: list[int], tasks: list[Task] | None = None,
                 prior_filter: int | None = None, status_filter: int | None = None):
        for source in sources:
            if not isinstance(source[0], TaskSource):
                raise TaskQueueError("нельзя передавать в очередь задач не объекты, " +
                                     "не реализующие контракт источника задач")
        self.sources = sources
        if any(ord_ >= len(sources) for ord_ in order):
            raise TaskQueueError("некорректный порядок обхода источников, индекс источника выходит за границы массива")
        self.order = order
        if tasks is not None:
            if any(not isinstance(task, Task) for task in tasks):
                raise TaskQueueError("нельзя передавать в очередь задач не объекты класса Task")
        self.tasks = tasks or []
        self.status_filter = status_filter
        self.prior_filter = prior_filter

    def __iter__(self) -> TaskIterator:
        sources = []
        for source in self.sources:
            sources.append(source[0](**source[1]))
        return TaskIterator(sources, self.order, self.tasks, self.prior_filter, self.status_filter)

    def push(self, task: Task):
        if not isinstance(task, Task):
            raise TaskQueueError("В очередь задач можно добавлять только задачи (класс Task)")
        self.tasks.append(task)

    def push_task_list(self, task_list: list[Task]):
        if not isinstance(task_list, Iterable):
            raise TaskQueueError("передан не Iterable объект")
        if any(not isinstance(task, Task) for task in task_list):
            raise TaskQueueError("нельзя передавать в очередь задач не объекты класса Task")
        for task in task_list:
            self.push(task)

    def pop(self):
        return self.tasks.pop(0)

    def get_generator(self) -> Generator[Task]:
        tasks = deepcopy(self.tasks) or []
        ended_sources = [0] * len(self.sources)
        sources = [source[0](**source[1]) for source in self.sources]
        pos = 0
        while sum(ended_sources) != len(self.sources) or len(tasks) > 0:
            if len(tasks) != 0:
                new_task = tasks.pop(0)
            else:
                new_task = Task.from_dict(sources[self.order[pos]].get_task())
                if sources[self.order[pos]].is_tasks_ended():
                    ended_sources[self.order[pos]] = 1
                pos = (pos + 1) % len(self.order)
                while ended_sources[self.order[pos]] and sum(ended_sources) != len(sources):
                    pos = (pos + 1) % len(self.order)
            if self.prior_filter:
                if new_task.priority != self.prior_filter:
                    continue
            if self.status_filter:
                if new_task.status != self.status_filter:
                    continue
            pushed_tasks = yield new_task
            if pushed_tasks is not None:
                if isinstance(pushed_tasks, Iterable):
                    if any(not isinstance(task, Task) for task in pushed_tasks):
                        raise TaskQueueError("нельзя передавать в очередь задач не объекты класса Task")
                    tasks.extend(pushed_tasks)
                else:
                    if not isinstance(pushed_tasks,Task):
                        raise TaskQueueError("нельзя передавать в очередь задач не объекты класса Task")
                    tasks.append(pushed_tasks)
