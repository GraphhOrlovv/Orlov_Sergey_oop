"""
======================================
1. Создай три класса: Cat, Dog, Duck.
В каждом реализуй метод speak(), возвращающий уникальную строку.
Создай список из экземпляров этих классов и вызови метод speak()
в цикле.
======================================"""

# class Dog:
#
#     def speak(self):
#         return "ГАВ ГАВ ГАВ"
#
# class Cat:
#
#     def speak(self):
#         return "МЯУ МЯУ МЯУ"
#
# class Duck:
#
#     def speak(self):
#         return "КРЯ КРЯ КРЯ"
#
# animals = [Dog(), Cat(), Duck()]
#
# for animal in animals:
#     print(animal.speak())

"""2. Создай базовый класс Shape
Создай три класса-наследника: Square, Rectangle, Triangle,
в каждом реализуй метод get_pr().
Проверь, что список shapes = [Square(...), Rectangle(...), Triangle(...)]
можно обойти в цикле и вызвать get_pr() у каждого.
======================================"""

# class Shape:
#     pass
#
# class Square(Shape):
#
#     def get_pr(self):
#         print("Метод get_pr у квадрата")
#
# class Rectangle(Shape):
#
#     def get_pr(self):
#         print("Метод get_pr у прямоугольника")
#
# class Triangle(Shape):
#
#     def get_pr(self):
#         print("Метод get_pr у треугольника")
#
# shapes = [Square(), Rectangle(), Triangle()]
# for shape in shapes:
#     shape.get_pr()

"""3. Сделай класс Shape абстрактным.
Переопредели get_pr() как @abstractmethod.
Попробуй создать объект класса Shape напрямую и убедись, что будет TypeError.
======================================"""

# from abc import ABC, abstractmethod
#
# class Shape(ABC):
#     @abstractmethod
#     def get_pr(self):
#         pass
#
# a = Shape() # Да, ошибка TypeError

"""4. Создай классы A, B, C, в каждом — свой __init__() с print("init A/B/C").
Наследуй D(A, B, C) и вызови super().__init__() в каждом __init__.
Выведи D.__mro__ и посмотри, в каком порядке вызываются инициализаторы.
======================================"""

# class A:
#     def __init__(self):
#         super().__init__()
#         print("init A")
#
# class B:
#     def __init__(self):
#         super().__init__()
#         print("init B")
#
# class C:
#     def __init__(self):
#         super().__init__()
#         print("init C")
#
# class D(A, B, C):
#     pass
#
# print(D.__mro__)
#
# d = D() # Иниты вызываюся в обратном порядке

"""5. Создай MixinLog (как в уроке).
Создай класс бронирования гостиницы (методы и атрибуты на свое усмотрение).
Создай класс, который наследует оба класса. Создай экземпляр этого класса.
======================================"""

import datetime

# class BookingHotel:
#
#     def __init__(self, room_class, floor_number, price_for_night):
#         if not 1 < floor_number < 31:
#             raise ValueError("Этаж не может быть меньше 1 и больше 30")
#         super().__init__()
#         self.room_class = room_class
#         self.floor_number = floor_number
#         self.price_for_night = price_for_night
#
#     def print_info(self):
#         print(f"Класс номера: {self.room_class}, этаж: {self.floor_number}, цена: {self.price_for_night} рублей")
#
# class MixinLog:
#     ID = 0
#     def __init__(self):
#         print("init MixinLog")
#         MixinLog.ID += 1
#         self.id = MixinLog.ID
#
#     def save_sell_log(self):
#         print(f"{self.id} забронирован в {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#
# class Notebook(BookingHotel, MixinLog):
#     pass
#
# n = Notebook("Business", 30, 10_000)
# n.print_info()
# n.save_sell_log()
# print()
# c = Notebook("Luxe", 5, 5_000)
# c.print_info()
# c.save_sell_log()

"""6. В Goods и MixinLog реализуй print_info().
Создай NoteBook(Goods, MixinLog) и проверь, какой метод вызывается.
Измени порядок наследования — изменилась ли логика?
======================================"""

# import datetime
#
# class BookingHotel:
#
#     def __init__(self, room_class: str, floor_number: int, price_for_night: int | float) -> None:
#         if not 1 < floor_number < 31:
#             raise ValueError("Этаж не может быть меньше 1 и больше 30")
#         super().__init__()
#         self.room_class = room_class
#         self.floor_number = floor_number
#         self.price_for_night = price_for_night
#
#     def print_info(self):
#         print(f"Класс номера: {self.room_class}, этаж: {self.floor_number}, цена: {self.price_for_night} рублей")
#
# class MixinLog:
#     ID = 0
#     def __init__(self):
#         print("init MixinLog")
#         MixinLog.ID += 1
#         self.id = MixinLog.ID
#         self.time_now = None
#
#     def save_sell_log(self):
#         self.time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         print(f"{self.id} забронирован в {self.time_now}")
#
#     def print_info(self):
#         print(f"ID номера: {self.id}, время создания брони: {self.time_now}")
#
# class Notebook(BookingHotel, MixinLog): # Если меняю порядок наследования, то возникает ошибка,
#                                         # так как MixinLog не принимает никакие аргументы, поэтому надо исправить это
#     pass
#
# n = Notebook("Business", 30, 10_000)
# n.print_info() # Сейчас вызывается метод у класса BookingHotel, так как он стоит раньше в MRO
# n.save_sell_log()

""" Исправим код """

# import datetime
#
# class BookingHotel:
#
#     def __init__(self, room_class: str, floor_number: int, price_for_night: int | float, **kwargs) -> None:
#         if not 1 < floor_number < 31:
#             raise ValueError("Этаж не может быть меньше 1 и больше 30")
#         super().__init__(**kwargs)
#         self.room_class = room_class
#         self.floor_number = floor_number
#         self.price_for_night = price_for_night
#
#     def print_info(self):
#         print(f"Класс номера: {self.room_class}, этаж: {self.floor_number}, цена: {self.price_for_night} рублей")
#
# class MixinLog:
#     ID = 0
#     def __init__(self, *args, **kwargs):
#         print("init MixinLog")
#         MixinLog.ID += 1
#         self.id = MixinLog.ID
#         self.time_now = None
#         super().__init__(*args, **kwargs)
#
#     def save_sell_log(self):
#         self.time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         print(f"{self.id} забронирован в {self.time_now}")
#
#     def print_info(self):
#         print(f"ID номера: {self.id}, время создания брони: {self.time_now}")
#
# class Notebook(MixinLog, BookingHotel):
#     pass
#
# n = Notebook("Business", 30, 10_000)
# n.save_sell_log()
# n.print_info() # Сейчас уже вызывается метод у класса MixinLog, так как он уже стоит раньше в MRO

"""======================================
Далее задания можете сделать через классы, функции или без них.
======================================
======================================
7. Напиши программу, которая запрашивает (из консоли) два числа и делит первое на второе.
Если второе число равно нулю — обработай ошибку (как называется ошибка найди сам)
и выведи сообщение: "На ноль делить нельзя!"
======================================"""

# def divide_2_nums() -> int | float | str:
#     try:
#         nums = input("Пожалуйста, введите 2 числа через пробел.\n"
#                      "Второе число не должно быть равно нулю: ").split()
#
#         if len(nums) != 2:
#             return "Ошибка ввода: нужно ввести ровно 2 числа"
#
#         num_1, num_2 = map(float, nums)
#         result = num_1 / num_2
#
#         return result
#
#     except ZeroDivisionError:
#         return "Ошибка: на ноль делить нельзя!!"
#     except ValueError:
#         return "Ошибка ввода: введите два числа через пробел"
#
# print(divide_2_nums())

"""8. Расширь программу из Задания 1:
Добавь обработку ошибки (как называется ошибка найди сам),
если пользователь ввёл не числа, а текст.
Выведи сообщение: "Ошибка ввода: введите два числа через пробел"
======================================"""

# Добавил обработку сразу в первом задании

"""9. Модифицируй код так, чтобы после обработки конкретных ошибок
был ещё один общий except, который перехватывает все остальные ошибки и выводит:
"Произошла неизвестная ошибка"
======================================"""

# def divide_2_nums() -> int | float | str:
#     try:
#         nums = input("Пожалуйста, введите 2 числа через пробел.\n"
#                      "Второе число не должно быть равно нулю: ").split()
#
#         if len(nums) != 2:
#             return "Ошибка ввода: нужно ввести ровно 2 числа"
#
#         num_1, num_2 = map(float, nums)
#         result = num_1 / num_2
#
#         return result
#
#     except ZeroDivisionError:
#         return "Ошибка: на ноль делить нельзя!!"
#     except ValueError:
#         return "Ошибка ввода: введите два числа через пробел"
#     except Exception as e:
#         return f"Произошла неизвестная ошибка: {e}"
#
# print(divide_2_nums())

"""10. При перехвате исключений из 7 и 8 заданий,
сохрани ошибку в переменную e и выведи её текст:
======================================"""

# Выполнил в предыдущем задании

"""11. Создай код, который ловит арифметические ошибки (ArithmeticError) в одном блоке.
Попробуй специально сделать ошибку деления на ноль или другую арифметическую ошибку.
======================================"""

# Если не обязательно писать на основе той же программы, которая в 9 задании, то можно сделать так:

# def test_arithmetic_errors(num_1: int | float, num_2: int | float) -> int | float | str:
#     try:
#         return num_1 / num_2
#         # return num_1 ** num_2 # Пытался вызвать арифметическую ошибку такого рода, но не получается, но всё равно оставил
#     except ArithmeticError as e:
#         return f"Неизвестная ошибка: {e}"
#
# print(test_arithmetic_errors(10, 0))

"""12. Запроси у пользователя два числа и выполни деление.
Если деление прошло успешно без ошибок — выведи
"Деление выполнено успешно" через (но не в блоке try)
======================================"""

# Если так считается, что это в блоке try, то можно ещё через флаг

# def divide_2_nums() -> int | float | str:
#
#     try:
#         nums = input("Пожалуйста, введите 2 числа через пробел.\n"
#                      "Второе число не должно быть равно нулю: ").split()
#
#         if len(nums) != 2:
#             return "Ошибка ввода: нужно ввести ровно 2 числа"
#
#         num_1, num_2 = map(float, nums)
#         result = num_1 / num_2
#
#     except ZeroDivisionError:
#         return "Ошибка: на ноль делить нельзя!!"
#     except ValueError:
#         return "Ошибка ввода: введите два числа через пробел"
#     except Exception as e:
#         return f"Произошла неизвестная ошибка: {e}"
#
#     else:
#         return f"Деление выполнено успешно\nРезультат: {result}"
#
# print(divide_2_nums())

"""13. Расширь код из Задания 12:
Добавь блок, в котором будет выводиться
"Работа программы завершена", независимо от успеха деления.
======================================"""

# def divide_2_nums() -> int | float | str:
#
#     try:
#         nums = input("Пожалуйста, введите 2 числа через пробел.\n"
#                      "Второе число не должно быть равно нулю: ").split()
#
#         if len(nums) != 2:
#             return "Ошибка ввода: нужно ввести ровно 2 числа"
#
#         num_1, num_2 = map(float, nums)
#         result = num_1 / num_2
#
#     except ZeroDivisionError:
#         return "Ошибка: на ноль делить нельзя!!"
#     except ValueError:
#         return "Ошибка ввода: введите два числа через пробел"
#     except Exception as e:
#         return f"Произошла неизвестная ошибка: {e}"
#
#     else:
#         return f"Деление выполнено успешно\nРезультат: {result}"
#
#     finally:
#         print("Работа программы завершена")
#
# print(divide_2_nums())

"""14. Реализуй две вложенные конструкции:
Внешний try/except обрабатывает неверный ввод (строки вместо чисел);
Внутренний try/except ловит деление на ноль.
======================================
15. Вынеси обработку деления в отдельную функцию divide(x, y)
с собственным try/except.
Во внешнем коде обработай только ошибку ввода.
"""