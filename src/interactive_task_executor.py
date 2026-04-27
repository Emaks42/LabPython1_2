import asyncio

from interactive_task_queue import read_sources
from src.handlers.printing_handler import PrintHandler
from src.handlers.unstable_handler import UnstableHandler
from src.handlers.configurable_handler import ConfigurableHandler
from src.handlers.basic_handler import BasicHandler
from src.handlers.chaos_handler import ChaosHandler
from src.distributors.maximizing_distributor import MaximizingDistributor
from src.distributors.random_distributor import RandomDistributor
from src.async_task_executor.async_executor import AsyncExecutor


def read_dict():
    inp___ = input("$ > ")
    inp__ = inp___.split(",")
    if any(":" not in s for s in inp__):
        print("некорректный формат записи")
        raise ValueError
    split_par = [i.split(":", 1) for i in inp__]
    par = {i[0].strip(): i[1] for i in split_par}
    return par


def read_handlers():
    handlers = {}
    print("Введите названия обработчиков, для окончания ввода верните end")
    inp_ = input("$ > ")
    while inp_ != "end":
        inp = inp_.split()
        if len(inp) != 2:
            print("некорректный ввод")
            inp_ = input("$ > ")
            continue
        if inp[0] in ["print", "unstable", "configurable", "basic", "chaos"] and inp[1].isdigit():
            if inp[0] == "configurable":
                print("введите параметры")
                try:
                    par = read_dict()
                except ValueError:
                    inp_ = input("$ > ")
                    continue
                handlers[ConfigurableHandler(par)] = int(inp[1])
            elif inp[0] == "chaos":
                print("введите параметры")
                try:
                    par = read_dict()
                except ValueError:
                    inp_ = input("$ > ")
                    continue
                handlers[ChaosHandler(par.get("seed"))] = int(inp[1])
            else:
                if inp[0] == "print":
                    handlers[PrintHandler()] = int(inp[1])
                if inp[0] == "unstable":
                    handlers[UnstableHandler()] = int(inp[1])
                if inp[0] == "basic":
                    handlers[BasicHandler()] = int(inp[1])
        inp_ = input("$ > ")
    return handlers


def read_distributor():
    print("Введите название распределителя и его параметры")
    while True:
        inp_ = input("$ > ")
        if inp_ == "none":
            return None
        if inp_ not in ["configurable", "random", "maximizing"]:
            print("неверное название")
            continue
        else:
            if inp_ == "random":
                print("введите параметры")
                try:
                    par = read_dict()
                except ValueError:
                    continue
                return RandomDistributor(par.get("seed"))
            elif inp_ == "maximizing":
                print("введите параметры")
                try:
                    par = read_dict()
                except ValueError:
                    continue
                if par.get("worker_param") is None:
                    print("некорректный ввод параметров")
                    continue
                return MaximizingDistributor(par["worker_param"], par.get("scaling_task_param"),
                                             par.get("buffer_size", 3))
            else:
                pass


async def run_async_executor(handlers, distributor, sources, order):
    async with AsyncExecutor(handlers, sources, order) as executor:
        if distributor is not None:
            executor.set_distributor(distributor)
        await executor.wait_all()


def interactive_task_executor():
    print("Добро пожаловать в интерактивный исполнитель задач")
    print("Введите источники, для окончания ввода напишите end")
    sources = read_sources()
    print("Введите порядок чтения источников в исполнителе:")
    while True:
        try:
            order = list(map(int, input().split()))
            break
        except ValueError:
            print("некорректный формат")
    distributor = read_distributor()
    handlers = read_handlers()
    print("Выполняется запуск асинхронного исполнителя задач")
    asyncio.run(run_async_executor(handlers, distributor, sources, order))
    print("Задачи успешно обработаны, результат можно увидеть в логах")
