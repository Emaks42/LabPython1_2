import datetime
from src.constants import POSSIBLE_STATUSES


class TaskError(Exception):
    ...


class FieldValidator:
    limitations: tuple[int, int] | list[str] | None
    type: type

    def __init__(self, lim, type_):
        self.limitations = lim
        self.type = type_

    def __call__(self, func):
        def foo(obj, val):
            if not isinstance(val, self.type):
                if isinstance(val, str):
                    val = self.type(val.strip())
                elif val is not None:
                    raise TaskError(f"значение {func.__name__} должно быть {self.type}")
            if isinstance(self.limitations, tuple):
                if not (self.limitations[0] < val < self.limitations[1]):
                    raise TaskError(
                        f"значение {func.__name__} должно быть в диапазоне от {self.limitations[0]} до " +
                        f"{self.limitations[1]}")
            elif isinstance(self.limitations, list):
                if val not in self.limitations:
                    raise TaskError(f"значение {func.__name__} должно быть в диапазоне {self.limitations}")
            func(obj, val)
        return foo


class Task:
    """
    Класс, описывающий задачу в системе
    """
    __slots__ = ('__id', '__description', '__priority', '__status', '__creation_time', '__deadline')

    def __init__(self, id_, description, priority, status, creation_time, deadline):
        self.__deadline = self.__priority = self.__status = self.__id = self.__description = None
        self.__creation_time = None
        self.id = id_
        self.description = description
        self.priority = priority
        self.status = status
        self.creation_time = creation_time
        self.deadline = deadline

    def __setattr__(self, key, value):
        if key[:2] == "__":
            raise TaskError("убедительная просьба не изменять скрытые атрибуты класса напрямую")
        super().__setattr__(key, value)

    def __getattribute__(self, item):
        if item[:2] == "__":
            raise TaskError("убедительная просьба не получать скрытые атрибуты класса напрямую")
        return super().__getattribute__(item)

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
    @FieldValidator(None, int)
    def id(self, val):
        self.__id = val

    @description.setter
    @FieldValidator(None, str)
    def description(self, val):
        self.__description = val

    @priority.setter
    @FieldValidator((0, 6), int)
    def priority(self, val):
        self.__priority = val

    @status.setter
    @FieldValidator(POSSIBLE_STATUSES, str)
    def status(self, val):
        self.__status = val

    @creation_time.setter
    @FieldValidator(None, datetime.datetime)
    def creation_time(self, val):
        self.__creation_time = val

    @deadline.setter
    @FieldValidator(None, datetime.datetime)
    def deadline(self, val):
        if val is None:
            self.__deadline = val
            return
        if val > self.creation_time:
            self.__deadline = val
        else:
            raise TaskError("Задача не должна иметь дедлайн раньше времени своего создания")

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

    def __str__(self):
        return f"Task. id: {self.id}, description: {self.description}, status: {self.status}, " \
               f"creation time: {self.creation_time}, priority: {self.priority}, deadline: {self.deadline}"
