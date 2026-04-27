import pytest
from src.handlers.basic_handler import BasicHandler
from src.handlers.printing_handler import PrintHandler
from src.async_task_executor.async_executor import AsyncExecutor
from src.distributors.random_distributor import RandomDistributor
from src.distributors.maximizing_distributor import MaximizingDistributor
from src.distributors.config_distributor import ConfigDistributor
from src.task_sources.generator_source import GeneratorSource
from src.task_working.task import Task


@pytest.mark.asyncio
async def test_random_distributor_work():
    async with AsyncExecutor({BasicHandler(): 5}, [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10})],
                             [0]) as executor:
        executor.set_distributor(RandomDistributor())
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()


@pytest.mark.asyncio
async def test_maximizing_distributor_work():
    async with AsyncExecutor({BasicHandler(): 5}, [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10})],
                             [0]) as executor:
        executor.set_distributor(MaximizingDistributor("delay", "priority"))
        await executor.send_task(Task.from_dict({"id": 10, "priority": 1}))
        await executor.wait_all()


@pytest.mark.asyncio
async def test_config_distributor_work():
    async with AsyncExecutor({BasicHandler(): 1, PrintHandler(): 1}) as executor:
        executor.set_distributor(ConfigDistributor({'priority': {
            2: {"delay": 0.01}
        }}))
        await executor.send_task(Task.from_dict({"id": 10, "priority": 2}))
        await executor.send_task(Task.from_dict({"id": 10}))
        await executor.wait_all()
