"""
Набор 03 — классы.
Темы: __init__ и валидация, @property, @classmethod, @staticmethod,
атрибуты класса и экземпляра, магические методы, наследование,
абстрактные классы, сравнение и сортировка объектов.

Как работать: пишешь код вместо `pass`, запускаешь  pytest -v test_tasks_03.py
Можно запускать по одной задаче:  pytest -v -k player   (или team, season, stage, user)
Стандартная библиотека разрешена: datetime, abc, functools и т. д.
"""
from datetime import date
from functools import total_ordering
from abc import ABC, abstractmethod


# ─── Задача 1. Игрок ──────────────────────────────────────────────────
class Player:
    """
    Player("Иванов Иван", date(2016, 5, 3))

    - name: пробелы по краям убрать, повторяющиеся пробелы внутри схлопнуть;
      пустое имя (или из одних пробелов) → ValueError.
    - birth_date: объект date; дата позже сегодняшнего дня → ValueError.

    Методы и свойства:
    - age_on(day: date) -> int — полных лет на указанную дату
        (день рождения в этот день уже считается: 3 мая 2026 → 10 лет).
    - свойство birth_year -> int.
    - can_play_in(division_year: int) -> bool — игрок может играть в дивизионе
        своего года рождения или СТАРШЕ (дивизион 2015 — для 2015 г. р. и младше).
        То есть True, если birth_year >= division_year.
    - @classmethod from_string("Иванов Иван;2016-05-03") — создать игрока из строки
        «ФИО;ГГГГ-ММ-ДД». Неверный формат → ValueError.
    - repr: Player('Иванов Иван', date(2016, 5, 3))
    - Два игрока равны, если совпадают имя (без учёта регистра) и дата рождения.
      Игроков можно класть в set (нужен __hash__, согласованный с __eq__).
    """
    def __init__(self, name: str, birth_date: date):
        if not name.strip():
            raise ValueError("Имя не может быть пустым или состоять из пробелов")
        else:
            self.name = ' '.join(name.split())
        if not isinstance(birth_date, date) or birth_date > date.today():
            raise ValueError("Дата рождения должна быть объектом date и не позже сегодняшнего дня")
        else:
            self.birth_date = birth_date

    def age_on(self, day: date) -> int:
        if not isinstance(day, date):
            raise TypeError("Аргумент должен быть объектом date")
        if (self.birth_date.month, self.birth_date.day) <= (day.month, day.day):
            return day.year - self.birth_date.year
        else:
            return day.year - self.birth_date.year - 1

    @property
    def birth_year(self) -> int:
        return self.birth_date.year

    def can_play_in(self, division_year: int) -> bool:
        if not isinstance(division_year, int):
            raise TypeError("Аргумент должен быть целым числом")
        return self.birth_year >= division_year

    @classmethod
    def from_string(cls, raw: str):
        try:
            name, birth_date_str = raw.split(';')
            birth_date = date.fromisoformat(birth_date_str)
        except Exception as e:
            raise ValueError("Ожидается 'ФИО;ГГГГ-ММ-ДД'") from e
        return cls(name, birth_date)

    def __repr__(self):
        d = self.birth_date
        return f"Player({self.name!r}, date({d.year}, {d.month}, {d.day}))"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.name.lower() == other.name.lower() and self.birth_date == other.birth_date

    def __hash__(self):
        return hash((self.name.lower(), self.birth_date))



# ─── Задача 2. Команда — свой контейнер ───────────────────────────────
class Team:
    """
    Team("Динамо Пресня")  — пустой состав.

    - Атрибут класса MAX_PLAYERS = 20 (общий для всех команд).
    - add(player) — добавить игрока:
        * игрок уже есть (по ==) → ValueError;
        * состав полон (MAX_PLAYERS) → ValueError.
    - remove(name) — удалить игрока по имени (без учёта регистра);
        нет такого → KeyError.
    - len(team)          → количество игроков;
    - player in team     → есть ли такой игрок (объект Player);
    - "иванов иван" in team → строку тоже можно проверять — по имени, без учёта регистра;
    - for p in team      → перебор игроков в порядке добавления;
    - team[0]            → игрок по индексу;
    - youngest()         → самый младший игрок (поздняя дата рождения); пустой состав → None.
    - str(team)          → "Динамо Пресня (3 игр.)"
    """
    MAX_PLAYERS = 20

    def __init__(self, name: str):
        self.name = name
        self.players = []

    def add(self, player: Player):
        if player in self.players:
            raise ValueError("Игрок уже есть в команде")
        if len(self.players) >= self.MAX_PLAYERS:
            raise ValueError("Состав команды полон")
        self.players.append(player)

    def remove(self, name: str):
        for player in self.players:
            if player.name.lower() == name.lower():
                self.players.remove(player)
                return
        raise KeyError("Игрок с таким именем не найден")

    def __len__(self):
        return len(self.players)

    def __contains__(self, item):
        if isinstance(item, Player):
            return item in self.players
        elif isinstance(item, str):
            return any(player.name.lower() == item.lower() for player in self.players)
        else:
            return False

    def __iter__(self):
        return iter(self.players)

    def __getitem__(self, index):
        return self.players[index]

    def youngest(self):
        if not self.players:
            return None
        return max(self.players, key=lambda player: player.birth_date)

    def __str__(self):
        return f"{self.name} ({len(self.players)} игр.)"

    
# ─── Задача 3. Сезон ──────────────────────────────────────────────────
@total_ordering
class Season:
    """
    Season("Зима 2027", date(2027, 1, 10), date(2027, 3, 28))

    - Пустое название → ValueError; окончание раньше начала → ValueError.
    - status_on(day: date) -> str:
        "Запланирован" — day раньше начала;
        "Идёт"         — day между началом и окончанием включительно;
        "Завершён"     — day позже окончания.
    - day in season  → True, если дата внутри сезона (границы включительно).
    - len(season)    → длительность в днях, включая оба крайних дня
                       (с 10 по 12 января — 3 дня).
    - Сезоны сортируются по дате начала: sorted(seasons) работает.
        Подсказка: нужен __lt__ (и __eq__); остальные сравнения можно получить
        декоратором functools.total_ordering.
    - Равны, если совпадают название, начало и окончание.
    """
    def __init__(self, name: str, start: date, end: date):
        if not name.strip():
            raise ValueError("Название сезона не может быть пустым или состоять из пробелов")
        if end < start:
            raise ValueError("Окончание сезона не может быть раньше начала")
        self.name = name
        self.start = start
        self.end = end

    def status_on(self, day:date) -> str:
        if day < self.start:
            return "Запланирован"
        elif self.start <= day <= self.end:
            return "Идёт"
        else:
            return "Завершён"

    def __contains__(self, day: date) -> bool:
        return self.start <= day <= self.end

    def __len__(self) -> int:
        return (self.end - self.start).days + 1

    def __lt__(self, other):
        if not isinstance(other, Season):
            return NotImplemented
        return self.start < other.start

    def __eq__(self, other):
        if not isinstance(other, Season):
            return NotImplemented
        return (self.name == other.name and
                self.start == other.start and
                self.end == other.end)

    def __hash__(self):
        return hash((self.name, self.start, self.end))


# ─── Задача 4. Этапы турнира: наследование ────────────────────────────
class Stage(ABC):
    """
    Базовый АБСТРАКТНЫЙ класс этапа. Создать Stage(...) напрямую нельзя → TypeError
    (используй abc.ABC и @abstractmethod).

    Stage.__init__(self, name, teams):
      - name — непустая строка, иначе ValueError;
      - teams — список названий команд; дубли (без учёта регистра) → ValueError;
      - после этого вызывает self.validate_teams() — проверку конкретного этапа.

    Абстрактные методы, которые реализует каждый наследник:
      - validate_teams()  — бросает ValueError, если число команд не подходит;
      - matches_count()   — сколько матчей будет сыграно в этапе.

    Наследники:
      Championship(name, teams, rounds=1) — чемпионат, «каждый с каждым» rounds раз;
          команд минимум 2; rounds ≥ 1, иначе ValueError;
          матчей: n * (n - 1) // 2 * rounds.
      PlayoffCup(name, teams) — кубок плей-офф: ровно 4 команды;
          матчей 4 (два полуфинала, финал, матч за 3-е место).
      RoundRobinCup(name, teams) — кубок «один круг»: ровно 3 команды; матчей 3.

    str(stage) → "<название>: <число команд> команд(ы), <число матчей> матч(ей)"
        например "Золотой кубок: 4 команд(ы), 4 матч(ей)" — один __str__ в базовом классе
        работает для всех наследников.
    """
    def __init__(self, name: str, teams: list[str]):
        if not name.strip():
            raise ValueError("Название этапа не может быть пустым")
        all_teams = [team.lower() for team in teams]
        if len(set(all_teams)) != len(teams):
            raise ValueError("Названия команд должны быть уникальными!")
        self.name = name
        self.teams = list(teams)
        self.validate_teams()

    @abstractmethod
    def validate_teams(self):
        pass

    @abstractmethod
    def matches_count(self):
        pass

    def __str__(self):
        return f"{self.name}: {len(self.teams)} команд(ы), {self.matches_count()} матч(ей)"


class Championship(Stage):

    def __init__(self, name: str, teams: list[str], rounds=1):
        self.rounds = rounds
        super().__init__(name, teams)

    def validate_teams(self):
        if len(self.teams) < 2:
            raise ValueError("Количество команд должно быть не менее 2")
        if self.rounds < 1:
            raise ValueError("Количество раундов должно быть не менее 1")

    def matches_count(self):
        n = len(self.teams)
        return n * (n - 1) // 2 * self.rounds

class PlayoffCup(Stage):

    def validate_teams(self):
        if len(self.teams) != 4:
            raise ValueError("Количество команд в данном этапе должно быть строго 4")

    def matches_count(self):
        return 4     

class RoundRobinCup(Stage):

    def validate_teams(self):
        if len(self.teams) != 3:
            raise ValueError("Количество команд в данном этапе должно быть строго 3")

    def matches_count(self):
        return 3



# ─── Задача 5. Пользователи админки ───────────────────────────────────
class User:
    """
    Учётные записи админки лиги.

    - Атрибут класса PERMISSIONS — словарь «роль → множество разрешённых действий»:
        "owner":        {"edit_score", "manage_seasons", "manage_users", "upload_photos"}
        "admin":        {"edit_score", "manage_seasons", "upload_photos"}
        "photographer": {"upload_photos"}
    - User(login, role):
        * login — без пробелов по краям, приводится к нижнему регистру, пустой → ValueError;
        * неизвестная роль → ValueError;
        * логин должен быть УНИКАЛЕН среди всех созданных пользователей
          (без учёта регистра) → ValueError при повторе.
          Подсказка: храни занятые логины в атрибуте КЛАССА.
    - can(action) -> bool — разрешено ли действие этой роли.
    - @classmethod reset() — очистить список занятых логинов (нужно тестам).
    - @staticmethod is_valid_password(password) -> bool — пароль годится, если:
        длина ≥ 8, есть хотя бы одна цифра, хотя бы одна буква в верхнем регистре
        и хотя бы одна в нижнем.
    - repr: User('sergey', role='owner')
    """
    PERMISSIONS = {
        "owner": {"edit_score", "manage_seasons", "manage_users", "upload_photos"},
        "admin": {"edit_score", "manage_seasons", "upload_photos"},
        "photographer": {"upload_photos"}
        }

    _logins = set()
    
    def __init__(self, login, role):
        if role not in self.PERMISSIONS:
            raise ValueError("Неизвестная роль!")
        if not login.strip():
            raise ValueError("Логин не может быть пустым!")
        new_login = login.strip().lower()
        if new_login in User._logins:
            raise ValueError("Такой логин уже занят!")
        
        self.role = role
        self.login = new_login
        User._logins.add(new_login)

    def can(self, action: str) -> bool:
        return action in self.PERMISSIONS[self.role]

    @classmethod
    def reset(cls):
        cls._logins.clear()

    @staticmethod 
    def is_valid_password(password) -> bool:
        has_len = len(password) >= 8
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        return all([has_len, has_upper, has_lower, has_digit])

    def __repr__(self):
        return f"User({self.login!r}, role={self.role!r})"

    
        



