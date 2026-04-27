import pytest
from src.handlers.printing_handler import PrintHandler
from src.handlers.basic_handler import BasicHandler
from src.handlers.configurable_handler import ConfigurableHandler
from src.handlers.chaos_handler import ChaosHandler
from src.handlers.unstable_handler import UnstableHandler
from src.async_task_executor.async_executor import AsyncExecutor
from src.task_sources.generator_source import GeneratorSource
from src.task_working.task import Task


@pytest.mark.asyncio
async def test_base_handler_work():
    async with AsyncExecutor({BasicHandler(): 5}, [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10})],
                             [0]) as executor:
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()


@pytest.mark.asyncio
async def test_configurable_handler_work():
    async with AsyncExecutor({ConfigurableHandler({"reverse_priority": True}): 5},
                             [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10})],
                             [0]) as executor:
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()


def absolute_print(inp):
    inp = inp + ""
    assert inp
    return


@pytest.mark.asyncio
async def test_printing_handler_work(monkeypatch):
    monkeypatch.setattr("builtins.print", absolute_print)
    async with AsyncExecutor({PrintHandler(): 5},
                             [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10})],
                             [0]) as executor:
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()


@pytest.mark.asyncio
async def test_unstable_handler_work():
    async with AsyncExecutor({UnstableHandler(): 5}) as executor:
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()


@pytest.mark.asyncio
async def test_chaos_handler_work():
    async with AsyncExecutor({ChaosHandler(): 5},
                             [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10})],
                             [0]) as executor:
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()
