"""
======================================
1. Создай две функции: inner() и outer().
В inner() вызови деление на ноль.
В outer() просто вызови inner().
Попробуй вызвать outer() без обработки ошибок и посмотри на стек вызовов.
======================================"""

# def inner():
#     a = 80 / 0
#     return a
#
# def outer():
#     inner()
#
# outer()

"""2. Добавь вокруг вызова outer() конструкцию try/except,
чтобы перехватить исключение и вывести сообщение
"Ошибка перехвачена на верхнем уровне".
======================================"""

# def inner():
#     a = 80 / 0
#     return a
#
# def outer():
#     inner()
#
# try:
#     outer()
# except ZeroDivisionError:
#     print("Ошибка перехвачена на верхнем уровне")

"""3. Перехвати исключение сразу в inner(), чтобы оно не поднималось дальше.
В случае ошибки возвращай строку "Ошибка в inner".
======================================"""

# def inner():
#     try:
#         a = 80 / 0
#         return a
#     except ZeroDivisionError:
#         return "Ошибка в inner"
#
# def outer():
#     result = inner()
#     return result
#
# print(outer())

"""4. Сделай так:
В inner() ошибка не перехватывается.
В outer() ошибка перехватывается через try/except.
В outer() при перехвате напечатай "Ошибка в outer".
======================================"""

# def inner():
#     a = 80 / 0
#     return a
#
# def outer():
#
#     try:
#         result = inner()
#     except ZeroDivisionError:
#         return "Ошибка в outer"
#     return result
#
# print(outer())

"""5. Напиши функцию get_value(), которая кидает ValueError.
Напиши тестовую функцию test_get_value(), которая:

Вызывает get_value();
Ловит ValueError;
Завершает тест с assert False, если исключение поймано.
======================================"""

# def get_value():
#     raise ValueError
#
# def test_get_value():
#     try:
#         get_value()
#     except ValueError:
#         assert False, "Ошибка!"
#
# test_get_value()

"""======================================
6. Создай функцию divide(x, y).
Если y == 0, выбрасывай ZeroDivisionError через raise.
Иначе возвращай результат деления.
======================================"""

# def divide(x, y):
#     if y == 0:
#         raise ZeroDivisionError
#     else:
#         return x / y
#
# print(divide(5, 0))

"""7. Создай функцию sqrt(x), которая:
Вызывает raise NegativeNumberError (пользовательское исключение), если x < 0;
Иначе возвращает квадратный корень из x.
Проверь поведение функции через try/except.
======================================"""

# class NegativeNumberError(Exception):
#     pass
#
# def sqrt(x):
#     if x < 0:
#         raise NegativeNumberError("Число не может быть меньше 0!")
#     else:
#         return x ** 0.5
#
# try:
#     print(sqrt(-1))
# except NegativeNumberError as e:
#     print(f"Ошибка: {e}")

"""8. Создай базовый класс MathError.
От него унаследуй:
NegativeNumberError
DivisionByZeroError
В функции safe_divide(x, y) выбрасывай DivisionByZeroError, если y == 0.
Проверь в try/except обработку ошибок через базовый класс MathError.
======================================"""

# class MathError(Exception):
#     pass
#
# class NegativeNumberError(MathError):
#     pass
#
# class DivisionByZeroError(MathError):
#     pass
#
# def safe_divide(x, y):
#     if y == 0:
#         raise DivisionByZeroError("Ошибка: На ноль делить нельзя!")
#     else:
#         return x / y
#
# try:
#     print(safe_divide(5, 0))
# except MathError as e:
#     print(e)

"""9. Создай тестовую функцию test_sqrt(), которая:
вызывает sqrt(x) с отрицательным числом;
перехватывает NegativeNumberError;
завершает тест с assert False и сообщением
"Нельзя брать корень из отрицательного числа".
======================================"""

# class NegativeNumberError(Exception):
#     pass
#
# def sqrt(x):
#     if x < 0:
#         raise NegativeNumberError("Число не может быть меньше 0!")
#     else:
#         return x ** 0.5
#
# def test_sqrt():
#     try:
#         sqrt(-5)
#     except NegativeNumberError:
#         assert False, "Нельзя брать корень из отрицательного числа"
#
# test_sqrt()

"""======================================
10. Открой файл sample.txt, прочитай его содержимое и выведи на экран.
Обеспечь закрытие файла через with.
======================================"""

# with open("sample.txt", "r") as f:
#     print(f.read())

"""11. Создай класс BackupList, который:
делает копию списка при входе в with,
при выходе сохраняет изменения, если ошибок не было,
откатывает изменения при ошибке.
Проверь:
успешное изменение списка;
откат при ошибке.
======================================
======================================
12. Создай декоратор-класс Timer,
который измеряет время выполнения функции и выводит результат.
"""