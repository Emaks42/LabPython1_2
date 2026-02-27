from dataclasses import dataclass
from protocol_source import TaskSource
from typing import Iterable


@dataclass
class Task:
    uid: int
    payload: str


def get_tasks_from_source(source: TaskSource) -> Iterable[Task]:
    if not isinstance(source, TaskSource):
        raise ValueError("incorrect data source")
    tasks: list[Task] = []
    while not source.is_tasks_ended():
        task = source.get_task()
        task = task.split(" - ", 1)
        try:
            tasks.append(Task(int(task[0]), task[1]))
        except ValueError:
            raise ValueError(f"corrupted task \"{' - '.join(task)}\"")
    return tasks
