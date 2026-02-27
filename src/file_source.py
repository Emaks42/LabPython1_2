from typing import TextIO
from os import SEEK_SET


class FileSource:
    """
    Источник данных файл
    :cvar file - исходный файл с задачами
    """
    file: TextIO

    def __init__(self, file: str):
        self.file = open(file, "r")

    def get_task(self) -> str:
        return self.file.readline()[:-1]

    def is_tasks_ended(self) -> bool:
        sav = self.file.tell()
        is_end = not bool(self.file.read())
        self.file.seek(sav, SEEK_SET)
        return is_end
