# Лабораторные работы 1-2 второй семестр

## Введение
В данной лабораторной работе был создан модуль приёма задач, способный работать с несколькими разными источниками
задач через единый контракт, также разработан класс задачи с достаточно безопасным публичным API


## Структура проекта

 <pre>
    .
    ├── LabPython1_2                           # Кодовая база лабораторной работы
    │   ├── src/                               # Исходный код
    │   ├── tests/                             # Unit тесты
    │   ├── uv.lock                            # зависимости проекта
    │   ├── .gitignore                         # git ignore файл
    │   ├──.pre-commit-config.yaml             # Средства автоматизации проверки кодстайла
    │   ├── README.md                          # Описание проекта
</pre>

В папке [src](./src) лежат файлы с реализацией задачи данной в лабораторной работы. Осонвным файлом является файл
[main.py](./src/main.py) в котором описана точка входа в приложение - функция **main**. Также в этой папке лежат файлы
[task_processing.py](src/task_working/task_processing.py), содержащий в себе функции приёма задач,
[task.py](src/task_working/task.py), в котором описывается класс задачи,
[protocol_source.py](src/task_sources/protocol_source.py), в котором с помощью Protocol описан общий поведенческий контракт для
испточников задач, три файла [api_source.py](src/task_sources/api_source.py), [generator_source.py](src/task_sources/generator_source.py) и
[file_source.py](src/task_sources/file_source.py), содержащие в себе описание классов источников задач (API, генератора и файла),
[constants.py](./src/constants.py) - константы, необходимые для работы программы (в основном для генераторов случайных
задач). Файл [file_](./src/file_) является файлом для проверки работы файлового источника задач.

В папке [tests](./tests) лежат **unit** тесты для проверки функциональности программы и её частей, а также несколько файлов
для тестирования чтения задач из файла.
Используется библиотека pytest. В файле [sources_test.py](./tests/sources_test.py) лежат тесты для источников задач,
а именно того, что они могут работать в стандартном режиме, в файле [task_test.py](./tests/task_test.py) находятся тесты для
проверки инкапсуляции класса задачи и её особых дескрипторов.
в файле [run_sim_test.py](./tests/task_getting_test.py) происходит проверка корректности работы чтения задач из источников.
Есть файл [conftest.py](./tests/conftest.py), задающий базовые фикстуры для тестов

В качестве пакетного менджера в данном репозитории используется [uv](https://github.com/astral-sh/uv).

## Допущения
<ul>
<li>API - источник данных, выдающий задачи в зависимости от времени обращения с некоторой задержкой</li>
<li>задачи, поступающие из источников имеют общий формат (Task { словарь }) и передаются как словари
(сделано, чтобы внешним источникам не требовались знания об устройстве класса Task)</li>
<li>не предполагается попытка чтения из недоступного файла (будет ошибка)</li>
</ul>

## Алгоритм решения
### CLI

CLI позволяет пользователю вводить одну из трёх команд:
<ul>
<li>listen_api [addr] - получить задачи из API</li>
<li>generate_tasks [seed] [amount] - генерирует amount задач по сиду seed, можно запускать без аргументов или только с
seed</li>
<li>read_file [filename] - читает задачи из файла</li>
</ul>

### Общий поведенческий контракт
Каждый источник данных должен содержать 2 функции:
<ul>
<li>get_task - возвращает одну задачу из источника (в текстовом формате)</li>
<li>is_tasks_ended - возвращает true или false в зависимости от того, закончились ли задачи в источнике</li>
</ul>
Такой набор функций был выбран, так как он на базовом уровне работает как поток ввода в почти любом языке программирования
следовательно удобен во взаимодействии.

### Источники задач
*Замечание:* у этих источников нет общего родительского класса

#### API
<ul>
<li>Получает на вход "адрес" сайта и согласно ему выбирает задержку получения задач (по сути просто берет хеш от
него и ставит последние несколько цифр как задержку)</li>
<li>При выдаче задачи делает некоторую задержку, после чего выдает задачу из константы API_ANSWERS в зависимости от
разницы между временем начала работы API и текущим временем</li>
<li>Конец потока задач определяется в зависимости от времени</li>
</ul>

#### Генератор
<ul>
<li>Получает на вход сид и количество задач, которые надо сгенерировать</li>
<li>При каждой выдаче задачи увеличивает внутренний счётчик количества задач, и когда он достигает требуемого
количества задач закрывает поток вывода (is_tasks_ended выдаёт true)</li>
<li>Задачи собираются по частям из констант TASK_PURPOSES и TASK_DESTINATIONS, идентификатор получается через хеш</li>
</ul>

#### Файл
<ul>
<li>На вход получает имя файла</li>
<li>Читает построчно задачи из файла</li>
<li>Конец задач - EOF</li>
</ul>

### Класс задачи
Задача является отдельным классом со следующими полями:
<ul>
<li>id - идентификатор задачи</li>
<li>description - описание задачи</li>
<li>priority - приоритет задачи от 1 до 5</li>
<li>creation_time - время создания</li>
<li>deadline - дедлайн задачи</li>
<li>status - статус задачи (возможные статусы описаны в константах)</li>
</ul>

**Замечание:** более подробно класс задачи описан в отдельном разделе ниже


### Функция чтения задач из файла
Алгоритм:
<ol>
<li>Проверить, закончились ли задачи в источнике</li>
<li>Получить задачу из источника</li>
</ol>
В результате получается список объектов типа Task

Также функция содержит следующие проверки:
<ul>
<li>Проверка на соответствие источника данных контракту</li>
<li>Проверка корректности задачи (подходит ли под вид uid - payload)</li>
</ul>
также есть версия функции, работающая как итератор, возвращающий задачи.

## Особенности реализации класса Task (задачи)

### Инкапсуляция
Инкапсуляция в классе реализована через property и специальный класс-декоратор
каждое поле класса имеет свою скрытую версию, доступную только через property (иначе будет исключение)

*Класс-декоратор:*
<pre>
class FieldValidator:
    limitations: tuple[int, int] | list[str] | None
    type: type

    def __init__(self, lim, type_):
        self.limitations = lim
        self.type = type_

    def __call__(self, func):
        def wrapper(obj, val):
            all_skip = False
            if not isinstance(val, self.type):
                if isinstance(val, str):
                    val = self.type(val.strip())
                elif val is not None:
                    raise TaskError(f"значение {func.__name__} должно быть {self.type}")
                if val is None:
                    all_skip = True
            if isinstance(self.limitations, tuple) and not all_skip:
                if not (self.limitations[0] < val < self.limitations[1]):
                    raise TaskError(
                        f"значение {func.__name__} должно быть в диапазоне от {self.limitations[0]} до " +
                        f"{self.limitations[1]}")
            elif isinstance(self.limitations, list) and not all_skip:
                if val not in self.limitations:
                    raise TaskError(f"значение {func.__name__} должно быть в диапазоне {self.limitations}")
            func(obj, val)
        return wrapper
</pre>

В этом классе описана обработка выхода за пределы ограничений нового значения атрибута и соответствия типов атрибута и
нового значения (None может быть значением в любом атрибуте)

*Пример сеттера для поля класса*

<pre>
@deadline.setter
@FieldValidator(None, datetime.datetime)
def deadline(self, val):
    if val is None or self.creation_time is None:
        self.__deadline = val
        return
    if val > self.creation_time:
        self.__deadline = val
    else:
        raise TaskError("Задача не должна иметь дедлайн раньше времени своего создания")
</pre>

### Защита от создания дополнительных атрибутов

Для этой цели используется slots, выделяющий фиксированный объём памяти под заранее определённые атрибуты

Доступ к самому slots болкируется и он неизменяем извне класса.

### Дополнительные возможности

Класс Task обладает:
<ol>
<li>
Двумя вычисляемыми атрибутами
<ul>
<li>is_outdated - просрочен ли дедлайн задачи</li>
<li>is_ready_to_work - можно ли начать выполнение задачи</li>
</ul>
</li>
<li>
Возможностью сборки объекта класса из словаря
</li>
</ol>

## Тестирование
Для тестирования используется модуль pytest. Также используется возможность pytest.fixture.

### Тестовые файлы

Тесты в каждом файле разделены по следующему принципу: сначала тесты базовой работы классов, дальше идёт тестирование ошибок.

### Конфигурационный файл тестов

<pre>
import pytest
import os


@pytest.fixture
def files():
    filenames = {"common": "tests"+os.sep+"common_file",
                 "corr_1": "tests"+os.sep+"corrupted_file_1",
                 "corr_2": "tests"+os.sep+"corrupted_file_2"}
    file_1 = open(filenames["common"], "w")
    file_1.write("""Task {
    id: 140
    description: обработать заказ с идентификатором 402
    priority: 5
    status: CREATED
    }
    Task {
    id: 1001
    description: отправить уведомление пользователю EMAKS
    priority: 2
    status: DONE
    }
    Task {
    id: 319
    description: проверить состояние сервиса eeva.team recroll.en
    priority: 1
    status: DONE
    }
    """)
    file_1.close()
    file_2 = open(filenames["corr_1"], "w")
    file_2.write("10a - f")
    file_2.close()
    file_3 = open(filenames["corr_2"], "w")
    file_3.write("""Task {
    something
    }""")
    file_3.close()
    return filenames
</pre>

В этом файле создаются базовые фикстуры для работы с файлами

### Примеры тестов

Тест корректности работы генераторного источника данных

<pre>
def test_generator_source_task_getting():
    source = GeneratorSource(10, 3)
    assert source.get_task() == {'description': 'перераспределить ресурсы на recroll.en', 'id': 2882, 'priority': 5,
                                 'status': 'CREATED'}
    assert not source.is_tasks_ended()
    assert source.get_task() == {'description': 'проверить состояние ресурса mai.ru goida.com', 'id': 1732,
                                 'priority': 2, 'status': 'CREATED'}
    assert not source.is_tasks_ended()
    assert source.get_task() == {'description': 'перераспределить ресурсы на eeva.team NIICHAVO.su', 'id': 1357,
                                 'priority': 3, 'status': 'DONE'}
    assert source.is_tasks_ended()
</pre>

Тест корректности обработки неверного формата задач

<pre>
def test_file_source_corrupted_files(files):
    with pytest.raises(ValueError):
        get_tasks_from_source(FileSource(files["corr_1"]))
    with pytest.raises(ValueError):
        get_tasks_from_source(FileSource(files["corr_2"]))
</pre>

Для тестирования используются дополнительные файлы из фикстуры.

Проверка обработки некорректных источников задач

<pre>
def test_task_getting_incorrect_sources():
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource1())
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource2())
    with pytest.raises(ValueError):
        get_tasks_from_source(IncorrectSource3())
    with pytest.raises(ValueError):
        get_tasks_from_source(12)
</pre>

Для этого теста используются дополнительные классы:

<pre>
#нет какой-либо функции
class IncorrectSource1:
    def __init__(self):
        self.abc = 0

    def get_task(self) -> str:
        return str(self.abc)


class IncorrectSource2:
    def __init__(self):
        self.a = True

    def is_tasks_ended(self) -> bool:
        return self.a

#неверный тип возвращаемого значения
class IncorrectSource3:
    def __init__(self):
        self.a = False

    def get_task(self):
        return self.a

    def is_tasks_ended(self) -> bool:
        return self.a
</pre>

Тестирование итератора

<pre>
def test_task_iter_base_work():
    source = GeneratorSource(10, 2)
    it = get_task_iter_from_source(source)
    assert it.__next__() == Task(2882, "перераспределить ресурсы на recroll.en", 5,
                                 "CREATED", None, None)
    assert it.__next__() == Task(1732,
                                 "проверить состояние ресурса mai.ru goida.com", 2,
                                 "CREATED", None, None)
</pre>

Тестирование отслеживания инкапсуляции задач

<pre>
def test_secret_attr_access():
    task_ = Task(100, 'отправить уведомление пользователю EMAKS', 2, "DONE", None, None)
    with pytest.raises(TaskError):
        task_.__id = 10
</pre>

Тестирование некорректных значений (выход за границы допустимых значений)

<pre>
def test_incorrect_limits():
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 2, "DOLNE",
             None, None)
    with pytest.raises(TaskError):
        Task(100, 'отправить уведомление пользователю EMAKS', 256, "DONE",
             None, None)
</pre>

*в первом случае используется несуществующий статус задачи, во втором приоритет за рамками [1;5]*

Все тесты в сумме покрывают примерно 96% кода из src. Всего есть ~14 тестов (так как размер и сложность кодовой базы
работы небольшие потребовалось небольшое количество тестов, отдельно хотелось бы отметить, что нет тестов для ошибок в
итераторе, так как его код почти не отличается от кода обычной функции получения задач).
