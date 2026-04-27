import random
import asyncio
import logging
from src.handlers.protocol_handler import Handler
from typing import Dict, Type, Any
from src.distributors.protocol_distributor import Distributor
from src.async_task_executor.async_task_queue import AsyncTaskQueue
from src.task_working.task import Task


class TaskProcessingError(Exception):
    def __init__(self, task: Task, handler_name: str, cause: Exception):
        self.task = task
        self.cause = cause
        super().__init__(f"[{task.id}] on handler {handler_name} by {cause}")


class AsyncExecutorError(Exception):
    ...


class AsyncExecutor:
    distributor: Distributor | None = None
    handlers: dict[Handler, int]

    def __init__(self, handlers: dict[Handler, int], sources: list[tuple[Type, Dict[str, Any]]] | None = None,
                 order: list[int] | None = None, qsize: int = 3,
                 log_config: dict[str, Any] | None = None):
        self.sources = sources or []
        self.order = order or []
        log_config = log_config or {"filename": "async.log", "level": logging.INFO,
                                    "format": "[%(asctime)s] %(message)s",
                                    "filemode": "w"}
        logging.basicConfig(**log_config)
        self.qsize = qsize
        self.handlers = handlers
        self._is_active = False
        self.seed = random.random()
        self._workers: list[asyncio.Task] = []
        self._errors: list[TaskProcessingError] = []

    def unpack_sources(self):
        sources = []
        main_seed = self.seed
        for source in self.sources:
            random.seed(self.seed)
            sources.append(source[0](**source[1]))
            self.seed = random.random()
        self.seed = main_seed
        return sources

    def set_distributor(self, dist: Distributor):
        if not isinstance(dist, Distributor):
            raise AsyncExecutorError("распределитель задач должен соблюдать протокол")
        self.distributor = dist

    async def send_task(self, task: Task):
        if not self._is_active:
            raise AsyncExecutorError("работа с асинхронным исполнителем задач должна вестись внутри контекстного"
                                     " менеджера")
        await self._queue.push(task)

    async def wait_all(self):
        await self._queue.join()

    async def __aenter__(self):
        self._queue = AsyncTaskQueue(self.qsize, self.unpack_sources(), self.order)
        self._is_active = True
        self._worker_tasks = []
        for handler, count in self.handlers.items():
            for i in range(count):
                self._worker_tasks.append(asyncio.create_task(self._worker_loop(f"worker-{i} on handler with params: "
                                                                                f"{handler.get_params()}", handler)))
                logging.info(f"started worker-{i} on handler with params: {handler.get_params()}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        await self.wait_all()
        for _ in self._worker_tasks:
            await self._queue.push(None)
        await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        self._is_active = False
        return False

    @property
    def errors(self):
        return self._errors

    async def _worker_loop(self, name: str, handler: Handler) -> None:
        while True:
            task = await self._queue.pop()
            logging.info(str(task))
            if task is None:
                logging.info(name + " ended")
                break
            if self.distributor is None:
                try:
                    logging.info(f"Task {str(task)}\n taken by {name}")
                    await handler.handle_task(task.as_dict())
                    logging.info(f"Task {str(task)}\n processed by {name}")
                except Exception as e:
                    error = TaskProcessingError(task, name, e)
                    logging.error(f"{error} on {name}\n during processing {task}")
                    self._errors.append(error)
                continue
            try:
                test = self.distributor.does_task_fit(task.as_dict(), handler.get_params())
                if test:
                    try:
                        logging.info(f"Task {str(task)}\n taken by {name}")
                        await handler.handle_task(task.as_dict())
                        logging.info(f"Task {str(task)}\n processed by {name}")
                    except Exception as e:
                        error = TaskProcessingError(task, name, e)
                        logging.error(f"{error} on {name}\n during processing {task}")
                        self._errors.append(error)
                else:
                    logging.info(f"task {task} unmatched {name}")
                    try:
                        self._queue.immediate_push(task)
                    except asyncio.QueueFull:
                        await self._queue.push(task)
            except Exception as e:
                logging.error(f"{e} on {name}\n during matching {task} and {name}")
                try:
                    logging.info(f"Task {str(task)}\n taken by {name}")
                    await handler.handle_task(task.as_dict())
                    logging.info(f"Task {str(task)}\n processed by {name}")
                except Exception as e:
                    error = TaskProcessingError(task, name, e)
                    logging.error(f"{error} on {name}\n during processing {task}")
                    self._errors.append(error)
