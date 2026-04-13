import pytest
from src.task_working.task_queue import TaskQueue, TaskQueueError
from src.task_sources.generator_source import GeneratorSource
from src.task_working.task import Task
from tests.task_getting_test import IncorrectSource1, IncorrectSource2
from src.constants import POSSIBLE_STATUSES, PRIORITY_LIMITATIONS


@pytest.fixture
def arr_queue():
    return TaskQueue([Task.from_dict({"id": 12}), Task.from_dict({"id": 13})])


@pytest.fixture
def source_queue():
    return TaskQueue([], [(GeneratorSource, {"amount_of_tasks": 3, "seed": 10}),
                          (GeneratorSource, {"amount_of_tasks": 2, "seed": 12})],
                     [0, 1, 1])


def test_base_work(arr_queue):
    arr_queue.push(Task.from_dict({"id": 14}))
    assert list(arr_queue) == [Task.from_dict({"id": 12}), Task.from_dict({"id": 13}), Task.from_dict({"id": 14})]
    assert arr_queue.pop() == Task.from_dict({"id": 12})
    assert arr_queue.pop() == Task.from_dict({"id": 13})
    arr_queue.push_task_list([Task.from_dict({"id": 15}), Task.from_dict({"id": 16})])
    assert arr_queue.pop() == Task.from_dict({"id": 14})
    assert arr_queue.pop() == Task.from_dict({"id": 15})


def test_source_pop(source_queue):
    source_queue.push(Task.from_dict({"id": 14}))
    assert source_queue.pop() == Task.from_dict({"id": 14})
    assert source_queue.pop() == Task.from_dict({"id": 2882, "description": "перераспределить ресурсы на recroll.en",
                                                 "status": "CREATED", "priority": 5})


def test_source_order_work(source_queue):
    it = iter(source_queue)
    assert next(it) == Task.from_dict({"id": 2882, "description": "перераспределить ресурсы на recroll.en",
                                      "status": "CREATED", "priority": 5})
    assert next(it) == Task.from_dict({"id": 1211, "description": "ожидать ответа от eeva.team recroll.en",
                                       "status": "DONE", "priority": 3})
    assert next(it) == Task.from_dict({"id": 3557,
                                       "description": "обработать входящие данные из внешнего источника "
                                                      "recroll.en EMAKS",
                                       "status": "CREATED", "priority": 3})
    assert next(it) == Task.from_dict({"id": 1732, "description": "проверить состояние ресурса mai.ru goida.com",
                                       "status": "CREATED", "priority": 2})
    assert next(it) == Task.from_dict({"id": 1357, "description": "перераспределить ресурсы на eeva.team NIICHAVO.su",
                                       "status": "DONE", "priority": 3})


def test_two_cycles(arr_queue):
    a = list(arr_queue)
    i, j = 0, 0
    for task1 in arr_queue:
        for task2 in arr_queue:
            assert task1 == a[i]
            assert task2 == a[j]
            j += 1
        j = 0
        i += 1


def test_incorrect_sources():
    with pytest.raises(TaskQueueError):
        TaskQueue([], [(IncorrectSource1, {})], [0])
    with pytest.raises(TaskQueueError):
        TaskQueue([], [(IncorrectSource2, {})], [0])


def test_incorrect_order():
    with pytest.raises(TaskQueueError):
        TaskQueue([], [(GeneratorSource, {})], [5])


def test_incorrect_task_list():
    with pytest.raises(TaskQueueError):
        TaskQueue([102], [(GeneratorSource, {})], [0])


def test_incorrect_push(arr_queue):
    with pytest.raises(TaskQueueError):
        arr_queue.push(1)
    with pytest.raises(TaskQueueError):
        arr_queue.push_task_list(1)
    with pytest.raises(TaskQueueError):
        arr_queue.push_task_list([10, 10])


def test_filters():
    tq = TaskQueue([], [(GeneratorSource, {"amount_of_tasks": 5, "seed": 10}),
                        (GeneratorSource, {"amount_of_tasks": 10, "seed": 12})],
                   [0, 1, 1])
    tq.prior_filter = PRIORITY_LIMITATIONS[0] + 1
    tq.status_filter = POSSIBLE_STATUSES[0]
    for task in tq:
        assert task.status == POSSIBLE_STATUSES[0]
        assert task.priority == PRIORITY_LIMITATIONS[0] + 1


def test_filter_validation(arr_queue):
    with pytest.raises(TaskQueueError):
        arr_queue.prior_filter = "-12"
    with pytest.raises(TaskQueueError):
        arr_queue.prior_filter = PRIORITY_LIMITATIONS[0] - 1
    with pytest.raises(TaskQueueError):
        arr_queue.status_filter = ""


def test_generator_working(source_queue):
    gen = source_queue.get_generator()
    assert next(gen) == Task.from_dict({"id": 2882, "description": "перераспределить ресурсы на recroll.en",
                                        "status": "CREATED", "priority": 5})
    assert gen.send(Task.from_dict({"id": 10})) == Task.from_dict({"id": 10})
    assert next(gen) == Task.from_dict({"id": 1211, "description": "ожидать ответа от eeva.team recroll.en",
                                       "status": "DONE", "priority": 3})


def test_generator_incorrect_send(source_queue):
    gen = source_queue.get_generator()
    next(gen)
    with pytest.raises(TaskQueueError):
        gen.send(10)
    gen = source_queue.get_generator()
    next(gen)
    with pytest.raises(TaskQueueError):
        gen.send("3023")
