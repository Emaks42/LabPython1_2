from typing import Protocol, runtime_checkable


@runtime_checkable
class TaskSource(Protocol):
    """
    Общий протокол для источников задач
    """
    def get_task(self) -> dict:
        ...

    def is_tasks_ended(self) -> bool:
        ...
