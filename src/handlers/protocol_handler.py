from typing import Protocol, runtime_checkable


@runtime_checkable
class Handler(Protocol):
    """
    Общий протокол для воркеров
    """
    async def handle_task(self, task: dict) -> dict:
        ...

    def get_params(self) -> dict:
        ...
