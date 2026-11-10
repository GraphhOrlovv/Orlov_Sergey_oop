"""
Набор 04. Декораторы.

Каждый декоратор можно написать ДВУМЯ способами:
  * функцией (внутренняя функция-обёртка, замыкание);
  * классом (__init__ принимает функцию, __call__ вызывает её).

Тесты проверяют только поведение, поэтому подойдёт любой вариант.
Лучшая тренировка — решить сначала функцией, потом переписать классом
и убедиться, что тесты всё ещё зелёные.

Во всех задачах обёрнутая функция должна сохранять своё имя и docstring
(__name__ и __doc__). Подсказка: functools.wraps для функции,
functools.update_wrapper(self, func) для класса.

Запуск: pytest -v test_tasks_04.py
Одна задача: pytest -v test_tasks_04.py -k count_calls
"""


# ---------------------------------------------------------------------------
# Задача 1. count_calls — счётчик вызовов
# ---------------------------------------------------------------------------
# Декоратор БЕЗ параметров. Считает, сколько раз вызвали функцию.
# Счётчик доступен как атрибут обёрнутой функции: func.calls
# Аргументы и результат передаются как есть.
#
#   @count_calls
#   def goal(player):
#       return f"Гол! {player}"
#
#   goal.calls            -> 0
#   goal("Петров")        -> "Гол! Петров"
#   goal("Иванов")
#   goal.calls            -> 2

import functools

# def count_calls(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         wrapper.calls += 1
#         result = func(*args, **kwargs)
#         return result
#     wrapper.calls = 0
#     return wrapper

""" Через класс """

class count_calls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

# ---------------------------------------------------------------------------
# Задача 2. require_role — проверка прав
# ---------------------------------------------------------------------------
# Декоратор С ПАРАМЕТРАМИ: @require_role("admin", "coach").
# Первый аргумент обёрнутой функции — пользователь с атрибутом .role.
# Если роль пользователя есть среди разрешённых — функция выполняется.
# Иначе — PermissionError с текстом:
#     "Роль 'viewer' не может выполнить publish_result"
# (в тексте роль пользователя и имя функции).
#
#   @require_role("admin", "coach")
#   def publish_result(user, match_id, score):
#       return f"{match_id}: {score}"
#
#   publish_result(admin, 7, "2:1")   -> "7: 2:1"
#   publish_result(viewer, 7, "2:1")  -> PermissionError

# def require_role(*roles):
#     def check_status(func):
#         @functools.wraps(func)
#         def wrapper(user, *args, **kwargs):
#             if user.role in roles:
#                 return func(user, *args, **kwargs)
#             raise PermissionError(f"Роль '{user.role}' не может выполнить {wrapper.__name__}")
#         return wrapper
#     return check_status

""" Через класс """

class require_role:
    def __init__(self, *roles):
        self.roles = roles

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.role in self.roles:
                return func(user, *args, **kwargs)
            raise PermissionError(f"Роль '{user.role}' не может выполнить {wrapper.__name__}")
        return wrapper

# ---------------------------------------------------------------------------
# Задача 3. retry — повтор при ошибке
# ---------------------------------------------------------------------------
# Декоратор С ПАРАМЕТРАМИ: @retry(times=3, exceptions=(ConnectionError,))
#   * вызывает функцию; если она упала с ошибкой из exceptions —
#     пробует снова, всего не больше times попыток;
#   * вернула результат — сразу возвращаем его;
#   * все попытки упали — пробрасываем ПОСЛЕДНЮЮ ошибку;
#   * ошибку не из exceptions НЕ повторяем, сразу пробрасываем;
#   * по умолчанию times=3, exceptions=(Exception,);
#   * times < 1 -> ValueError сразу при создании декоратора.
# Это типичная вещь в автотестах: «флакающий» запрос к API.
#
#   @retry(times=3, exceptions=(ConnectionError,))
#   def get_table():
#       ...   # падает дважды, на третий раз отдаёт таблицу

# def retry(times=3, exceptions=(Exception,)):
#     if times < 1:
#         raise ValueError("Изначально попыток не может быть меньше 1")
    
#     def try_func(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             left_times = times
#             last_exc = None
#             while left_times >= 1:
#                 left_times -= 1
#                 try:
#                     return func(*args, **kwargs)
#                 except exceptions as e:
#                     last_exc = e
#                     if left_times:
#                         print(f"Ошибка: {last_exc}, попыток осталось {times}")
#             raise last_exc
#         return wrapper
#     return try_func

""" Через класс """
class retry:
    def __init__(self, times=3, exceptions=(Exception,)):
        if times < 1:
            raise ValueError("Изначально попыток не может быть меньше 1")
        self.times = times
        self.exceptions = exceptions

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, self.times + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    if attempt == self.times:
                        raise 
                    print(f"Попытка {attempt} из {self.times} не удалась, ошибка: {e}")
        return wrapper

# ---------------------------------------------------------------------------
# Задача 4. memoize — кэш результатов
# ---------------------------------------------------------------------------
# Декоратор БЕЗ параметров. Запоминает результат для набора аргументов
# и при повторном вызове с теми же аргументами возвращает его из кэша,
# не вызывая функцию.
# Достаточно поддержать только позиционные аргументы (они хешируемые).
# Атрибуты обёрнутой функции:
#   func.hits        — сколько раз результат взят из кэша;
#   func.clear()     — очистить кэш и обнулить hits.
#
#   @memoize
#   def team_rating(team_id):
#       ...           # «дорогой» подсчёт
#
#   team_rating(1); team_rating(1); team_rating(2)
#   team_rating.hits  -> 1

# def memoize(func):

#     cache = {}

#     @functools.wraps(func)
#     def wrapper(*args):
#         if args in cache:
#             wrapper.hits += 1
#             return cache[args]
#         result = func(*args)
#         cache[args] = result
#         return result

#     wrapper.hits = 0

#     def clear():
#         cache.clear()
#         wrapper.hits = 0

#     wrapper.clear = clear
#     return wrapper

""" Через класс """
class memoize:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.cache = {}
        self.hits = 0

    def __call__(self, *args):
        if args in self.cache:
            self.hits += 1
            return self.cache[args]
        result = self.func(*args)
        self.cache[args] = result
        return result

    def clear(self):
        self.cache.clear()
        self.hits = 0

    
    
        
        
