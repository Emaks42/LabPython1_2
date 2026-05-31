from src.task_sources.file_source import FileSource
from src.task_sources.api_source import APISource
from src.task_sources.generator_source import GeneratorSource
from src.task_working.task_queue import TaskQueue, TaskQueueError
from src.task_working.task import Task


def read_sources():
    inp_ = input("$ > ")
    sources = []
    while inp_ != "end":
        inp = inp_.split()
        if len(inp) == 0:
            inp_ = input("$ > ")
            continue
        if inp[0] == "read_file":
            if len(inp) == 1:
                print("недостаточно аргументов")
            elif len(inp) == 2:
                print("Файл добавлен")
                sources.append((FileSource, {"file": inp[1]}))
            else:
                print("слишком много аргументов")
        elif inp[0] == "listen_api":
            if len(inp) == 1:
                print("недостаточно аргументов")
            elif len(inp) == 2:
                print("Апи добавлен")
                sources.append((APISource, {"address": inp[1]}))
            else:
                print("слишком много аргументов")
        elif inp[0] == "generate_tasks":
            if len(inp) > 3:
                print("слишком много аргументов")
            else:
                print("Генератор добавлен")
                if len(inp) == 1:
                    sources.append((GeneratorSource, {}))
                if len(inp) == 2:
                    sources.append((GeneratorSource, {"amount_of_tasks": int(inp[1])}))
                elif len(inp) == 3:
                    sources.append((GeneratorSource, {"amount_of_tasks": int(inp[1]),
                                                      "seed": int(inp[2])}))
        else:
            print("неизвестный источник задач")
        inp_ = input("$ > ")
    return sources


def read_tasks():
    tasks = []
    print("Введите задачи, для окончания ввода верните end")
    inp_ = input("$ > ")
    while inp_ != "end":
        inp = inp_.split(",")
        if any(":" not in s for s in inp):
            print("некорректный формат записи задачи")
        split_par = [i.split(":", 1) for i in inp]
        par = {i[0].strip(): i[1] for i in split_par}
        tasks.append(Task.from_dict(par))
        inp_ = input("$ > ")
    print("ввод задач завершён")
    return tasks


def interactive_generator(gen):
    print("Запущен режим интерактивного генератора, для окончания введите end")
    inp_ = input("$ > ")
    while inp_ != "end":
        inp = inp_.split()
        if len(inp) == 0:
            inp_ = input("$ > ")
            continue
        if inp[0] == "send":
            tasks = read_tasks()
            print(gen.send(tasks))
        elif inp[0] == "next":
            print(next(gen))
        else:
            print("неизвестная команда")
        inp_ = input("$ > ")


def interactive_task_queue():
    print("Пожалуйста введите источники задач для очереди, для окончания ввода напишите end")
    sources = read_sources()
    print("Введите порядок чтения источников в очереди:")
    while True:
        try:
            order = list(map(int, input().split()))
            break
        except ValueError:
            print("некорректный формат")
    tasks = read_tasks()
    tq = TaskQueue(tasks, sources, order)
    print("Запущен режим интерактивной очереди, для окончания введите end")
    inp_ = input("$ > ")
    while inp_ != "end":
        inp = inp_.split()
        if len(inp) == 0:
            inp_ = input("$ > ")
            continue
        if inp[0] == "push":
            tasks = read_tasks()
            tq.push_task_list(tasks)
        elif inp[0] == "pop":
            print(tq.pop())
        elif inp[0] == "print":
            print(*tq)
        elif inp[0] == "filter":
            if len(inp) < 3:
                print("недостаточно аргументов")
            elif len(inp) > 3:
                print("слишком много аргументов")
            else:
                if inp[1] not in ["priority", "status"]:
                    print("неверное название изменяемой переменной")
                else:
                    if inp[2] == "remove":
                        if inp[1] == "priority":
                            tq.prior_filter = None
                        else:
                            tq.status_filter = None
                    else:
                        try:
                            if inp[1] == "priority":
                                tq.prior_filter = int(inp[2])
                            else:
                                tq.status_filter = inp[2]
                        except ValueError:
                            print("некорректный ввод")
                        except TaskQueueError:
                            print("значение за рамками допустимых")
        elif inp[0] == "gen":
            interactive_generator(tq.get_generator())
        else:
            print("неизвестная команда")
        inp_ = input("$ > ")
