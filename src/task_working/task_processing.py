from src.task_sources.protocol_source import TaskSource
from src.task_working.task import Task


def get_tasks_from_source(source: TaskSource) -> list[Task]:
    """
    Функция, получающая задачи из источника, описанного протоколом
    :param source: источник данных
    :return: список задач
    """
    if not isinstance(source, TaskSource):
        raise ValueError("incorrect data source")
    tasks: list[Task] = []
    while not source.is_tasks_ended():
        task = source.get_task()
        if not isinstance(task, dict):
            raise ValueError(f"incorrect type of task, expected dict, got \"{type(task)}\"")
        tasks.append(Task.from_dict(task))
    return tasks


def get_task_iter_from_source(source: TaskSource):
    """
        Функция, получающая задачи из источника, описанного протоколом
        :param source: источник данных
        :return: итератор
    """
    if not isinstance(source, TaskSource):
        raise ValueError("incorrect data source")
    while not source.is_tasks_ended():
        task = source.get_task()
        if not isinstance(task, dict):
            raise ValueError(f"incorrect type of task, expected dict, got \"{type(task)}\"")
        yield Task.from_dict(task)
