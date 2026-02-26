from src.file_source import FileSource
from src.api_source import APISource
from src.generator_source import GeneratorSource


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    file = FileSource("file_")
    while not file.is_tasks_ended():
        print(file.get_task())
    api = APISource("goida.com")
    while not api.is_tasks_ended():
        print(api.get_task())
    gener = GeneratorSource(15, 12)
    while not gener.is_tasks_ended():
        print(gener.get_task())


if __name__ == "__main__":
    main()
