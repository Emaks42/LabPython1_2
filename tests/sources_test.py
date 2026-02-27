from src.file_source import FileSource
from src.generator_source import GeneratorSource
from src.api_source import APISource


def test_file_source_task_getting(files):
    source = FileSource(files["common"])
    assert source.get_task() == "103 - проверить состояние ресурса MAII"
    assert not source.is_tasks_ended()
    assert source.get_task() == "3457 - проверить состояние сервиса mai.ru NIICHAVO.su"
    assert not source.is_tasks_ended()
    assert source.get_task() == "104 - обработать заказ с идентификатором 40"
    assert source.is_tasks_ended()


def test_generator_source_task_getting():
    source = GeneratorSource(10, 3)
    assert source.get_task() == "1139 - перераспределить ресурсы на recroll.en"
    assert not source.is_tasks_ended()
    assert source.get_task() == "1305 - обработать входящие данные из внешнего источника EMAKS goida.com"
    assert not source.is_tasks_ended()
    assert source.get_task() == "3332 - отправить уведомление пользователю mai.ru"
    assert source.is_tasks_ended()


def test_api_source_task_getting():
    source = APISource("goida.com")
    assert source.get_task()[:2] + source.get_task()[3:6] == "10 - "
    while not source.is_tasks_ended():
        assert True
