from src.task_sources.file_source import FileSource
from src.task_sources.generator_source import GeneratorSource
from src.task_sources.api_source import APISource


def test_file_source_task_getting(files):
    source = FileSource(files["common"])
    assert source.get_task() == {'description': 'обработать заказ с идентификатором 402', 'id': '140', 'priority': '5',
                                 'status': 'CREATED'}
    assert not source.is_tasks_ended()
    assert source.get_task() == {'description': 'отправить уведомление пользователю EMAKS', 'id': '1001',
                                 'priority': '2', 'status': 'DONE'}
    assert not source.is_tasks_ended()
    assert source.get_task() == {'description': 'проверить состояние сервиса eeva.team recroll.en', 'id': '319',
                                 'priority': '1', 'status': 'DONE'}
    assert source.is_tasks_ended()


def test_generator_source_task_getting():
    source = GeneratorSource(10, 3)
    assert source.get_task() == {'description': 'перераспределить ресурсы на recroll.en', 'id': 2882, 'priority': 5,
                                 'status': 'CREATED'}
    assert not source.is_tasks_ended()
    assert source.get_task() == {'description': 'проверить состояние ресурса mai.ru goida.com', 'id': 1732,
                                 'priority': 2, 'status': 'CREATED'}
    assert not source.is_tasks_ended()
    assert source.get_task() == {'description': 'перераспределить ресурсы на eeva.team NIICHAVO.su', 'id': 1357,
                                 'priority': 3, 'status': 'DONE'}
    assert source.is_tasks_ended()


def test_api_source_task_getting():
    source = APISource("goida.com")
    assert 100 < source.get_task()["id"] < 106
    while not source.is_tasks_ended():
        assert True
