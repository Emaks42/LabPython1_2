from typing import Protocol, runtime_checkable


@runtime_checkable
class Distributor(Protocol):
    """
    Общий протокол для распределителя задач
    """
    def does_task_fit(self, task: dict, worker_params: dict) -> bool:
        ...
