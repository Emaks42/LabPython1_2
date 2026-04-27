from src.task_sources.file_source import FileSource
from src.task_sources.api_source import APISource
from src.task_sources.generator_source import GeneratorSource
from src.task_working.task_processing import get_tasks_from_source
from src.interactive_task_queue import interactive_task_queue
from src.interactive_task_executor import interactive_task_executor


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    print("Добро пожаловать в командную строку обработчика задач, для завершения введите end")
    inp_ = input("$ > ")
    while inp_ != "end":
        inp = inp_.split()
        if len(inp) == 0:
            inp_ = input("$ > ")
            continue
        if inp[0] == "read_file":
            if len(inp) == 1:
                print("недостаточно аргументов")
            elif len(inp) == 2:
                print("Данные из файла:")
                file = FileSource(inp[1])
                print(*get_tasks_from_source(file), sep="\n")
            else:
                print("слишком много аргументов")
        elif inp[0] == "listen_api":
            if len(inp) == 1:
                print("недостаточно аргументов")
            elif len(inp) == 2:
                print("Данные из апи:")
                api = APISource(inp[1])
                print(*get_tasks_from_source(api), sep="\n")
            else:
                print("слишком много аргументов")
        elif inp[0] == "generate_tasks":
            if len(inp) > 3:
                print("слишком много аргументов")
            else:
                print("Данные из генератора:")
                gener = GeneratorSource()
                if len(inp) == 2:
                    gener = GeneratorSource(int(inp[1]))
                elif len(inp) == 3:
                    gener = GeneratorSource(int(inp[1]), int(inp[2]))
                print(*get_tasks_from_source(gener), sep="\n")
        elif inp[0] == "tq":
            interactive_task_queue()
        elif inp[0] == "exec":
            interactive_task_executor()
        else:
            print("неизвестная команда")
        inp_ = input("$ > ")
    print("спасибо, что выбираете нас 😁")


if __name__ == "__main__":
    main()
