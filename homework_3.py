"""
======================================
1. Создай класс Circle, в котором:
есть атрибуты класса MIN_RADIUS = 1 и MAX_RADIUS = 1000,
метод класса is_valid_radius(cls, r), который проверяет, входит ли значение в допустимый диапазон.
Проверь результат вызова:
print(Circle.is_valid_radius(500))   # True
print(Circle.is_valid_radius(1500))  # False
======================================"""
import math

# class Circle:
#     MIN_RADIUS = 1
#     MAX_RADIUS = 1000
#
#     @classmethod
#     def is_valid_radius(cls, radius):
#         return cls.MIN_RADIUS <= radius <= cls.MAX_RADIUS
#
# print(Circle.is_valid_radius(500))
# print(Circle.is_valid_radius(1500))

"""2. Добавь в класс Circle:
статический метод area(radius),
который возвращает площадь круга по формуле π * r ** 2 (используй импорт math.pi),
инициализацию в __init__, которая сохраняет радиус,
только если он проходит валидацию через метод is_valid_radius()
(подумай как можно проверить значения перед тем как записать их в переменные экземпляра класса)
Пример:
c = Circle(10)
print(c.area(c.radius))  # Площадь круга
======================================"""

import math

# class Circle:
#     MIN_RADIUS = 1
#     MAX_RADIUS = 1000
#
#     @classmethod
#     def is_valid_radius(cls, radius: int | float) -> bool:
#         return cls.MIN_RADIUS <= radius <= cls.MAX_RADIUS
#
#     def __init__(self, radius: int | float) -> None:
#         assert Circle.is_valid_radius(radius),\
#             f'Радиус должен быть в пределах от {Circle.MIN_RADIUS} до {Circle.MAX_RADIUS}'
#         self.radius = radius
#
#     @staticmethod
#     def area(radius: int | float) -> str:
#         return f'Площадь круга равна: {round(math.pi * radius ** 2, 3)}'
#
# circle_1 = Circle(5.5)
# print(circle_1.area(circle_1.radius))

"""3. Расширь Circle, добавив обычный метод print_info, который выводит:
Радиус: ...
Допустимый диапазон: [MIN, MAX]
Метод должен использовать и self, и атрибуты класса через type(self).

Пример вызова:
c.print_info()
======================================"""

# import math
#
# class Circle:
#     MIN_RADIUS = 1
#     MAX_RADIUS = 1000
#
#     @classmethod
#     def is_valid_radius(cls, radius: int | float) -> bool:
#         return cls.MIN_RADIUS <= radius <= cls.MAX_RADIUS
#
#     def __init__(self, radius: int | float) -> None:
#         assert Circle.is_valid_radius(radius),\
#             f'Радиус должен быть в пределах от {Circle.MIN_RADIUS} до {Circle.MAX_RADIUS}'
#         self.radius = radius
#
#     @staticmethod
#     def area(radius: int | float) -> str:
#         return f'Площадь круга равна: {round(math.pi * radius ** 2, 3)}'
#
#     def print_info(self):
#         print(f'Радиус: {self.radius}\n'
#               f'Допустимый диапазон: [{type(self).MIN_RADIUS}, {type(self).MAX_RADIUS}]\n')
#
# c = Circle(8)
# c.print_info()

"""4. Создай класс User, в котором:

приватные атрибуты __login и __password;
метод set_credentials(login, password), который сохраняет их только если оба значения — строки;
метод get_credentials(), который возвращает кортеж из логина и пароля.
Попробуй создать объект и изменить логин снаружи напрямую. Проверь, что это не сработает.
======================================"""

# class User:
#
#     def __init__(self) -> None:
#         self.__login = None
#         self.__password = None
#
#     def set_credential(self, login: str, password: str) -> None:
#         assert (isinstance(login, str) and isinstance(password, str)),\
#             'Логин и/или пароль не являются строками!'
#         self.__login = login
#         self.__password = password
#
#     def get_credentials(self) -> tuple[str, str]:
#         return self.__login, self.__password
#
# user_1 = User()
#
# user_1.set_credential('ivan@mail.ru', 'qwerty')
#
# print(f"Логин и пароль пользователя user_1: {user_1.get_credentials()}\n")
#
# user_1.__login = 'wefewfwe'# Создаёт новый атрибут __login, проверим:
# print(user_1.__dict__, '\n')
#
# print(user_1.__login, '\n')
#
# print(f"Логин и пароль пользователя user_1: {user_1.get_credentials()}\n") # Ничего не изменилось

"""5. Добавь в User:

метод check_password(password) — возвращает True,
если переданное значение совпадает с сохранённым паролем;
приватный метод __encrypt_password(password),
который возвращает пароль в верхнем регистре (имитация шифрования);
в set_credentials вызывай __encrypt_password.
Пример:
u = User()
u.set_credentials("daniil", "qwerty")
print(u.check_password("qwerty"))      # True
print(u.check_password("qwe"))         # False
======================================"""

# class User:
#
#     def __init__(self) -> None:
#         self.__login = None
#         self.__password = None
#
#     @staticmethod
#     def __encrypt_password(password: str) -> str:
#         return password.upper()
#
#     def set_credential(self, login: str, password: str) -> None:
#         assert (isinstance(login, str) and isinstance(password, str)),\
#             'Логин и/или пароль не являются строками!'
#         self.__login = login
#         self.__password = self.__encrypt_password(password)
#
#     def get_credentials(self) -> tuple[str, str]:
#         return self.__login, self.__password
#
#     def check_password(self, password) -> bool:
#         return self.__password == self.__encrypt_password(password)
#
# user_1 = User()
#
# user_1.set_credential('ivan@mail.ru', 'qwerty')
#
# print(f"Логин и пароль пользователя user_1: {user_1.get_credentials()}\n")
#
# print(user_1.check_password("qwerty"))
# print(user_1.check_password("qwe"))

"""6. Убедись, что приватный метод __encrypt_password нельзя вызвать извне.
Попробуй это сделать — и поясни результат.
Также выведи напрямую u.__password — и проверь, что будет ошибка.

Попробуй добраться до данных через u._User__password
"""

# class User:
#     "Класс для создания пользователя с логином и паролем"
#     def __init__(self) -> None:
#         self.__login = None
#         self.__password = None
#
#     @staticmethod
#     def __encrypt_password(password: str) -> str:
#         return password.upper()
#
#     def set_credential(self, login: str, password: str) -> None:
#         assert (isinstance(login, str) and isinstance(password, str)),\
#             'Логин и/или пароль не являются строками!'
#         self.__login = login
#         self.__password = self.__encrypt_password(password)
#
#     def get_credentials(self) -> tuple[str, str]:
#         return self.__login, self.__password
#
#     def check_password(self, password) -> bool:
#         return self.__password == self.__encrypt_password(password)
#
# user_1 = User()
#
# user_1.set_credential('ivan@mail.ru', 'qwerty')
#
# print(f"Логин и пароль пользователя user_1: {user_1.get_credentials()}\n")
#
# print(user_1.check_password("qwerty"))
# print(user_1.check_password("qwe"))
#
# # user_1.__encrypt_password('asdfg') # Python не понимает, что за метод, так как он приватный
#
# print(f"Логин и пароль пользователя user_1: {user_1.get_credentials()}\n")
#
# # print(user_1.__password) # Пишет, что такого атрибута нет
#
# print(user_1._User__password) # Подчёркивает и ругается, но пароль выводит, но так делать нельзя