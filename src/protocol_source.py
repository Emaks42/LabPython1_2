from typing import Protocol, runtime_checkable


@runtime_checkable
class TaskSource(Protocol):

    def get_task(self) -> str:
        ...

    def is_tasks_ended(self) -> bool:
        ...
