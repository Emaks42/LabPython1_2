import pytest
from src.file_source import FileSource
from src.generator_source import GeneratorSource
from src.task_processing import get_tasks_from_source, Task


class IncorrectSource1:
    def __init__(self):
        self.abc = 0

    def get_task(self) -> str:
        return str(self.abc)


class IncorrectSource2:
    def __init__(self):
        self.a = True

    def is_tasks_ended(self) -> bool:
        return self.a


def test_task_getting_base_work():
    source = GeneratorSource(10, 2)
    assert get_tasks_from_source(source) == [Task(1139, "перераспределить ресурсы на recroll.en"),
                                    Task(1305, "обработать входящие данные из внешнего источника EMAKS goida.com")]


def test_task_getting_incorrect_sources():
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource1())
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource2())
    with pytest.raises(ValueError):
        get_tasks_from_source(12)


def test_file_source_corrupted_files(files):
    with pytest.raises(ValueError):
        get_tasks_from_source(FileSource(files["corr_1"]))
    with pytest.raises(ValueError):
        get_tasks_from_source(FileSource(files["corr_2"]))
