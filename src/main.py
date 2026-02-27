from src.file_source import FileSource
from src.api_source import APISource
from src.generator_source import GeneratorSource
from src.task_processing import get_tasks_from_source


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    print("Данные из файла:")
    file = FileSource("file_")
    print(*get_tasks_from_source(file), sep="\n")

    print("\nДанные из апи:")
    api = APISource("goida.com")
    print(*get_tasks_from_source(api), sep="\n")

    print("\nДанные из генератора:")
    gener = GeneratorSource(15, 12)
    print(*get_tasks_from_source(gener), sep="\n")


if __name__ == "__main__":
    main()
