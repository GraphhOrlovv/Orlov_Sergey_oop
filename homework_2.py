"""
======================================
1. Создай класс Person с методом set_data(self, name, age), который сохраняет имя и возраст в объект.
Добавь метод get_data(self), который возвращает строку вида "Имя: <name>, Возраст: <age>".
Создай два объекта и задай им разные значения. Выведи информацию по каждому.
======================================"""

# class Person:
#
#     def set_data(self, name: str, age: int):
#         self.name= name
#         self.age = age
#
#     def get_data(self) -> str:
#         return f"Имя: {self.name}, Возраст: {self.age}"
#
# person_1 = Person()
# person_2 = Person()
#
# person_1.set_data('Олег', 30)
# person_2.set_data('Максим', 20)
#
# print(person_1.get_data())
# print(person_2.get_data())

"""2. Добавь в класс Point методы set_coords(x, y) и get_coords().
Создай объект p, задай координаты (7, 12), а затем получи и выведи их.
После этого измени координаты на (-3, 5) и снова выведи результат через get_coords().
======================================"""

# class Point:
#
#     def set_coords(self, x: int | float, y: int | float) -> None:
#         self.x = x
#         self.y = y
#
#     def get_coords(self) -> str:
#         return f"Координаты объекта: {self.x, self.y}"
#
# p = Point()
#
# p.set_coords(7, 12)
# print(p.get_coords())
# print()
# p.set_coords(-3, 5)
# print(p.get_coords())

"""3. Используя getattr(), получи ссылку на метод get_coords у объекта Point и вызови его.
Проверь, что результат совпадает с обычным вызовом p.get_coords().
======================================"""

# class Point:
#
#     def set_coords(self, x: int | float, y: int | float) -> None:
#         self.x = x
#         self.y = y
#
#     def get_coords(self) -> str:
#         return f"Координаты объекта: {self.x, self.y}"
#
# p = Point()
#
# p.set_coords(7, 12)
# res = p.get_coords()
# print(res, '\n')
#
# result = getattr(p, 'get_coords')
# print(result(), '\n')
#
# print("Результаты выводов совпадают" if result() == res else "Что-то не так")

"""4. Создай класс Person, в котором метод __init__() принимает имя и возраст и сохраняет их как атрибуты объекта.
Добавь метод show_info(), который выводит строку "Имя: <name>, возраст: <age>". Создай объект и вызови метод.
======================================"""

# class Person:
#
#     def __init__(self, name: str, age: int | float) -> None:
#         self.name = name
#         self.age = age
#
#     def show_info(self) -> None:
#         print(f"Имя: {self.name}, возраст: {self.age}")
#
# person_1 = Person('Олег', 25)
#
# person_1.show_info()

"""5. Добавь в класс Person метод __del__(), который выводит сообщение "Удалён объект: <имя>",
где <имя> — значение поля name. Создай и удали объект вручную с помощью del.
======================================"""

# class Person:
#
#     def __init__(self, name: str, age: int | float) -> None:
#         self.name = name
#         self.age = age
#
#     def show_info(self) -> None:
#         print(f"Имя: {self.name}, возраст: {self.age}")
#
#     def __del__(self):
#         print(f"Удалён объект {self.name}")
#
# person_1 = Person('Илья', 30)
# print()
# person_1.show_info()
#
# person_2 = Person('Ваня', 18)
# del person_2
# # person_2.show_info() # Не получится, так как такого объекта уже нет

"""6. Создай класс Rectangle с инициализацией по умолчанию: ширина 1, высота 1.
Добавь метод area(), который возвращает площадь прямоугольника.
Проверь работу с прямоугольником без аргументов и с заданной шириной и высотой.
======================================"""

# class Rectangle:
#
#     def __init__(self, width: int | float =1, height: int | float =1) -> None:
#         self.width = width
#         self.height = height
#
#     def area(self) -> int | float:
#         return self.width * self.height
#
# rectangle_1 = Rectangle()
#
# print(f"Площадь прямоугольника с заданной шириной {rectangle_1.width} "
#       f"и высотой {rectangle_1.height} равна: {rectangle_1.area()}\n")
#
# rectangle_2 = Rectangle(3, 5)
#
# print(f"Площадь прямоугольника с шириной {rectangle_2.width} "
#       f"и высотой {rectangle_2.height} равна: {rectangle_2.area()}")

"""7. Создай класс Logger, который всегда возвращает один и тот же объект.
При создании экземпляра в __new__ выводи Создание логгера,
а при вызове __init__ — Инициализация логгера.
======================================
"""

# class Logger:
#     instance = None
#
#     def __new__(cls, *args, **kwargs):
#         print("Создание логгера")
#         if cls.instance is None:
#             cls.instance = super().__new__(cls)
#         return cls.instance
#
#     def __init__(self):
#         print("Инициализация логгера")
#
# object_1 = Logger()
#
# object_2 = Logger()
#
# print(id(object_1))
#
# print(id(object_2))