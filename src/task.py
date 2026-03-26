import datetime
from src.constants import POSSIBLE_STATUSES


class TaskError(Exception):
    ...


class Task:
    """
    Класс, описывающий задачу в системе
    """
    __slots__ = ('__id', '__description', '__priority', '__status', '__creation_time', '__deadline')

    def __init__(self, id_, description, priority, status, creation_time, deadline):
        self.id = id_
        self.description = description
        self.priority = priority
        self.status = status
        self.deadline = deadline
        self.creation_time = creation_time

    def __setattr__(self, key, value):
        if key[:2] == "__":
            raise TaskError("убедительная просьба не изменять скрытые атрибуты класса напрямую")
        super().__setattr__(key, value)

    def __getattribute__(self, item):
        if item[:2] == "__":
            raise TaskError("убедительная просьба не получать скрытые атрибуты класса напрямую")
        super().__getattribute__(item)

    @property
    def id(self) -> int | None: return self.__id

    @property
    def deadline(self) -> datetime.datetime | None: return self.__deadline

    @property
    def creation_time(self) -> datetime.datetime | None: return self.__creation_time

    @property
    def description(self) -> str | None: return self.__description

    @property
    def priority(self) -> int | None: return self.__priority

    @property
    def status(self) -> str | None: return self.__status

    @id.setter
    def id(self, val):
        if val is None:
            self.__id = val
            return
        if isinstance(val, int):
            self.__id = val
        else:
            raise TaskError("значение id должно быть int")

    @description.setter
    def description(self, val):
        if val is None:
            self.__description = val
            return
        if isinstance(val, str):
            self.__description = val
        else:
            raise TaskError("значение id должно быть str")

    @priority.setter
    def priority(self, val):
        if val is None:
            self.__priority = val
            return
        if isinstance(val, int):
            if 0 < val < 6:
                self.__description = val
            else:
                raise TaskError("значение priority должно быть в диапазоне от 1 до 5")
        else:
            raise TaskError("значение priority должно быть int")

    @status.setter
    def status(self, val):
        if val is None:
            self.__status = val
            return
        if val in POSSIBLE_STATUSES:
            self.__status = val
        else:
            raise TaskError(f"значение status должно быть в диапазоне {POSSIBLE_STATUSES}")

    @creation_time.setter
    def creation_time(self, val):
        if val is None:
            self.__creation_time = val
            return
        if isinstance(val, datetime.datetime):
            self.__creation_time = val
        else:
            raise ValueError("значение creation_time должно быть в формате datetime.datetime")

    @deadline.setter
    def deadline(self, val):
        if val is None:
            self.__deadline = val
            return
        if isinstance(val, datetime.datetime):
            if val > self.creation_time:
                self.__deadline = val
            else:
                raise TaskError("Задача не должна иметь дедлайн раньше времени своего создания")
        else:
            raise ValueError("значение deadline должно быть в формате datetime.datetime")

    @property
    def is_outdated(self):
        if self.deadline is None:
            raise TaskError("Не указан deadline")
        return datetime.datetime.now() > self.deadline

    @property
    def is_ready_to_work(self):
        if self.status is None:
            raise TaskError("Не указан status")
        return self.status == POSSIBLE_STATUSES[0] and (not self.is_outdated)

    @classmethod
    def from_dict(cls, dict_):
        return cls(dict_.get("id"), dict_.get("description"), dict_.get("priority"),
                   dict_.get("status"), dict_.get("creation_time"), dict_.get("deadline"))
