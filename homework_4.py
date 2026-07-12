"""
======================================
1. Создай класс SecureData, который:

имеет атрибут __secret, задаваемый в __init__;
переопределяет __getattribute__, чтобы при попытке получить __secret извне выбрасывать ValueError;
внутри класса доступ к __secret должен работать.
Проверь:
data = SecureData("пароль123")
print(data.__secret)      # ошибка
print(data.get_secret())  # "пароль123"
======================================"""

# class SecureData:
#
#     def __init__(self, secret):
#         self.__secret = secret
#
#     def get_secret(self):
#         return self.__secret
#
#     def __getattribute__(self, name):
#         if name == "__secret":
#             raise ValueError("Это секретные данные! Просто так их получить не получится)")
#         return object.__getattribute__(self, name)
#
# data = SecureData("пароль123")
# print(data.get_secret())
# print(data.__secret)

"""2. Добавь в класс SecureData метод __setattr__,
который запрещает создание любого атрибута с именем token.

Проверь:
data.token = "abc123"  # ❌ AttributeError
data.other = "ok"      # ✅ работает
======================================"""

# class SecureData:
#
#     def __init__(self, secret):
#         self.__secret = secret
#
#     def get_secret(self):
#         return self.__secret
#
#     def __getattribute__(self, name):
#         if name == "__secret":
#             raise ValueError("Ошибка")
#         return object.__getattribute__(self, name)
#
#     def __setattr__(self, key, value):
#         if key == 'token':
#             raise AttributeError(f"Имя атрибута не может быть '{key}'")
#         object.__setattr__(self, key, value)
#
# data = SecureData("пароль123")
# print(data.get_secret())
#
# # data.token = "abc123"
# data.other = "ok"
#
# print(data.__dict__) # Проверил, правильно ли я всё понимаю


"""3. Создай класс SafeDict, в котором:

нет атрибута default;
реализован __getattr__, который возвращает "N/A" (это строка) при попытке получить несуществующий атрибут;
реализован __delattr__, который пишет "Удалён атрибут <имя>" и действительно удаляет атрибут.
Проверь:
d = SafeDict()
print(d.unknown)     # "N/A"
d.key = 10
del d.key            # "Удалён атрибут key"
======================================"""

# class SafeDict:
#
#     def __getattr__(self, name):
#         return "N/A"
#
#     def __delattr__(self, name):
#         print(f"Удалён атрибут {name}")
#         object.__delattr__(self, name)
#
# d = SafeDict()
# print(d.unknown)
# d.key = 10
# print(d.__dict__)
# del d.key
# print(d.__dict__)

"""4. Создай класс Employee с приватными полями __name и __salary.
Добавь @property для поля salary, а также сеттер с валидацией:

зарплата должна быть положительным числом;
если нет — выбрасывать ValueError.
Проверь, что:
e = Employee("Daniil", 5000)
print(e.salary)   # 5000
e.salary = 8000
print(e.salary)   # 8000
e.salary = -100   # ❌ ValueError
======================================"""

# class Employee:
#
#     def __init__(self, name, salary):
#         self.__name = name
#         self.__salary = salary
#
#     @property
#     def salary(self):
#         return self.__salary
#
#     @salary.setter
#     def salary(self, value):
#         if value < 0:
#             raise ValueError(f"Зарплата должна быть положительной, а получено '{value}'!")
#         self.__salary = value
#
# e = Employee("Daniil", 5000)
# print(e.salary,'\n')
# e.salary = 8000
# print(e.salary)
# e.salary = -100

"""5. Добавь @deleter для поля salary, чтобы при удалении выводилось "зарплата удалена"
и поле реально исчезало.
Проверь:

del e.salary
print(e.__dict__)  # salary нет"""

# class Employee:
#
#     def __init__(self, name, salary):
#         self.__name = name
#         self.__salary = salary
#
#     @property
#     def salary(self):
#         return self.__salary
#
#     @salary.setter
#     def salary(self, value):
#         if value < 0:
#             raise ValueError(f"Зарплата должна быть положительной, а получено '{value}'!")
#         self.__salary = value
#
#     @salary.deleter
#     def salary(self):
#         print("Зарплата удалена")
#         del self.__salary
#
#
# e = Employee("Daniil", 5000)
# print(e.salary,'\n')
# e.salary = 8000
# print(e.salary)
#
# del e.salary
#
# print(e.__dict__)

"""6. Представь, что ты пишешь обёртку над HTML-формой.
Создай класс LoginForm с полем username, которое реализовано через @property.

Логика:
геттер возвращает self._username
сеттер добавляет лог "username изменён"
Проверь, что:
form = LoginForm()
form.username = "admin"  # выводит лог
print(form.username)     # "admin"
======================================"""

# class LoginForm:
#
#     @property
#     def username(self):
#         return self.__username
#
#     @username.setter
#     def username(self, name):
#         print(f"Username изменён на {name}")
#         self.__username = name
#
# form = LoginForm()
# form.username = "admin"
# print(form.username)

"""7. Создай класс Card, где:
поле __number хранит номер карты (строка);
в @property возвращай номер с маской **** **** **** 1234;
в @setter проверяй, что номер состоит из 16 цифр;
в @deleter логируй удаление номера с текущим временем.
Напиши тесты (через assert)
проверку установки корректного номера;
проверку исключения при вводе короткого номера;
проверку вывода замаскированного номера.
======================================"""

# from datetime import datetime
#
# class Card:
#
#     @property
#     def number(self):
#         num = str(self.__number)
#         return "**** " * 3 + num[-4:]
#
#     @number.setter
#     def number(self, num):
#         if len(str(num)) != 16:
#             raise ValueError("Номер карты должен состоять ровно из 16 цифр!")
#         self.__number = str(num)
#
#     @number.deleter
#     def number(self):
#         print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}: Удалён номер карты.')
#         del self.__number

"""Тесты: """

"""Тест 1:"""
#
# card_1 = Card()
# card_1.number = 1234567891234567
# assert card_1._Card__number == '1234567891234567', "Номер не сохранился"
# print(card_1.number)
#
# print("Тест 1 на установку корректного номера пройден.")

"""Тест 2:"""
# try:
#     card_1 = Card()
#     card_1.number = 123456789123456
#     assert False, "Ожидалось исключение, но его не было"
# except ValueError as e:
#     assert str(e) == "Номер карты должен состоять ровно из 16 цифр!", "Тест не пройден"
#     print("Тест 2 на попытку ввести короткий номер пройден.")

"""Тест 3:"""
# card_1 = Card()
# card_1.number = 3487654909123465
# assert card_1.number == '**** **** **** 3465', "Номер не зашифрован"
# print(card_1.number)
#
# print("Тест 3 на проверку вывода замаскированного номера пройден.")

"""8. Создай класс UserData для API регистрации пользователя:
email — строка, содержит @;
age — целое число ≥ 18;
is_active — bool;
свойство .json возвращает словарь для запроса.
Напиши тест (через assert)
проверь, что при age = 15 выбрасывается ValueError;
проверь, что email без @ вызывает ошибку;
проверь, что json возвращает корректную структуру.

"""

# class UserData:
#
#     def __init__(self, email, age, is_active):
#         self.__email = email
#         self.__age = age
#         self.__is_active = is_active
#
#     @property
#     def email(self):
#         if '@' not in self.__email:
#             raise NameError("Email должен содержать символ '@'")
#         return self.__email
#
#     @email.setter
#     def email(self, name_email):
#         if '@' not in name_email:
#             raise NameError("Email должен содержать символ '@'")
#         self.__email = name_email
#
#     @property
#     def age(self):
#         if not isinstance(self.__age, int) or self.__age < 18:
#             raise ValueError("Возраст не может быть нецелым или меньше 18")
#         return self.__age
#
#     @age.setter
#     def age(self, num):
#         if not isinstance(num, int) or num < 18:
#             raise ValueError("Возраст не может быть нецелым или меньше 18")
#         self.__age = num
#
#     @property
#     def is_active(self):
#         if not isinstance(self.__is_active, bool):
#             raise TypeError("is_active должен быть булевым значением")
#         return self.__is_active
#
#     @is_active.setter
#     def is_active(self, value):
#         if not isinstance(value, bool):
#             raise TypeError("is_active должен быть булевым значением")
#         self.__is_active = value
#
#     @property
#     def json(self):
#         if '@' not in self.__email:
#             raise NameError("Email должен содержать символ '@'")
#         if not isinstance(self.__age, int) or self.__age < 18:
#             raise ValueError("Возраст не может быть нецелым или меньше 18")
#         if not isinstance(self.__is_active, bool):
#             raise TypeError("is_active должен быть булевым значением")
#         return {
#             "email": self.__email,
#             "age": self.__age,
#             "is_active": self.__is_active
#         }

"""Тесты: """

"""Тест 1: """

# user_1 = UserData('vanya@yandex.ru', 18, True)
# try:
#     user_1.age = 15
#     assert False, "Здесь ожидалась ошибка, но её не было"
# except ValueError as e:
#     assert str(e) == "Возраст не может быть нецелым или меньше 18", "Тест не пройден"
#     print(user_1.age)
#     print("Тест 1 на проверку присвоения невалидного возраста пройден")

"""Тест 2: """

# user_1 = UserData('vanya@yandex.ru', 18, True)
# try:
#     user_1.email = 'eqhowflkmgoierqg'
#     assert False, "Здесь ожидалась ошибка, но её не было"
# except NameError as e:
#     assert str(e) == "Email должен содержать символ '@'", "Тест не пройден"
#     print(user_1.email)
#     print("Тест 2 на проверку присвоения невалидного почтового адреса пройден")

"""Тест 3: """

# user_1 = UserData('vanya@yandex.ru', 18, True)
# assert isinstance(user_1.json, dict), "json не возвращает словарь"
# print(user_1.json)
# print("Тест 3 на проверку возврата json корректной структуры пройден")
