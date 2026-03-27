import pytest
from src.file_source import FileSource, FileSourceError
from src.generator_source import GeneratorSource
from src.task_processing import get_tasks_from_source, Task, get_task_iter_from_source


class IncorrectSource1:
    def __init__(self):
        self.abc = 0

    def get_task(self) -> dict:
        return {20320: 10}


class IncorrectSource2:
    def __init__(self):
        self.a = True

    def is_tasks_ended(self) -> bool:
        return self.a


class IncorrectSource3:
    def __init__(self):
        self.a = False

    def get_task(self):
        return self.a

    def is_tasks_ended(self) -> bool:
        return self.a


def test_task_getting_base_work():
    source = GeneratorSource(10, 2)
    gen = get_tasks_from_source(source)
    assert gen[0] == Task(2882, "перераспределить ресурсы на recroll.en", 5,
                          "CREATED", None, None)
    assert gen[1] == Task(1732,
                          "проверить состояние ресурса mai.ru goida.com", 2,
                          "CREATED", None, None)


def test_task_iter_base_work():
    source = GeneratorSource(10, 2)
    it = get_task_iter_from_source(source)
    assert it.__next__() == Task(2882, "перераспределить ресурсы на recroll.en", 5,
                                 "CREATED", None, None)
    assert it.__next__() == Task(1732,
                                 "проверить состояние ресурса mai.ru goida.com", 2,
                                 "CREATED", None, None)


def test_task_getting_incorrect_sources():
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource1())
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource2())
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource3())
    with pytest.raises(ValueError):
        get_tasks_from_source(12)


def test_file_source_corrupted_files(files):
    with pytest.raises(FileSourceError):
        get_tasks_from_source(FileSource(files["corr_1"]))
    with pytest.raises(FileSourceError):
        get_tasks_from_source(FileSource(files["corr_2"]))
