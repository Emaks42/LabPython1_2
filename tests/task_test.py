import pytest
from src.task import Task, TaskError
from datetime import datetime


def test_task_base_work():
    t1 = datetime.now()
    t2 = datetime.now()
    assert Task.from_dict({'description': 'отправить уведомление пользователю EMAKS', 'id': '1001', 'priority': '2',
                           'status': 'DONE', "creation_time": t1, "deadline": t2}) == \
                            Task(1001, 'отправить уведомление пользователю EMAKS', 2, "DONE", t1, t2)


def test_incorrect_types():
    with pytest.raises(TaskError):
        Task(10.0, 'отправить уведомление пользователю EMAKS', 2, "DONE",
             None, None)
    with pytest.raises(TaskError):
        Task(100, len('отправить уведомление пользователю EMAKS'), 2, "DONE",
             None, None)
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 2.0, "DONE",
             None, None)
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 2, len("DONE"),
             None, None)
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 2, "DONE",
             -1, 3)
    with pytest.raises(TaskError):
        Task(10.0, 'отправить уведомление пользователю EMAKS', 2, len("DONE"),
             datetime.now(), 3)


def test_incorrect_limits():
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 2, "DOLNE",
             None, None)
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 256, "DONE",
             None, None)


def test_special_conditions():
    t = datetime.now()
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 2, "DONE",
             datetime.now(), t)


def test_secret_attr_access():
    task_ = Task(100, 'отправить уведомление пользователю EMAKS', 2, "DONE", None, None)
    with pytest.raises(TaskError):
        task_.__id = 10


def test_special_options():
    task_ = Task(100, 'отправить уведомление пользователю EMAKS', 2, "CREATED", None, datetime.now())
    assert task_.is_outdated
    task_ = Task(100, 'отправить уведомление пользователю EMAKS', 2, "CREATED", None,
                 datetime.fromisocalendar(2077, 1, 1))
    assert task_.is_ready_to_work


def test_special_options_errors():
    task_ = Task(100, 'отправить уведомление пользователю EMAKS', 2, None, None, None)
    with pytest.raises(TaskError):
        assert task_.is_ready_to_work
    with pytest.raises(TaskError):
        assert task_.is_outdated
