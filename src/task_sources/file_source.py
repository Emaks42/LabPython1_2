from typing import TextIO
from os import SEEK_SET


class FileSourceError(Exception):
    ...


class FileSource:
    """
    Источник данных файл
    :cvar file - исходный файл с задачами
    """
    file: TextIO

    def __init__(self, file: str):
        self.file = open(file, "r")

    def get_task(self) -> dict:
        text = self.file.readline()[:-1]
        if text != "Task {":
            raise FileSourceError("некорректный формат записи task")
        task = dict()
        text = self.file.readline()[:-1]
        while text != "}":
            if ":" not in text:
                raise FileSourceError("некорректный формат записи полей task")
            k = text.split(":", 1)
            task[k[0]] = k[1].strip()
            text = self.file.readline()[:-1]
        return task

    def is_tasks_ended(self) -> bool:
        sav = self.file.tell()
        is_end = not bool(self.file.read())
        self.file.seek(sav, SEEK_SET)
        return is_end
