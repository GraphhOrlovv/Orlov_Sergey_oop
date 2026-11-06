import copy
"""
Набор 02 — списки словарей, сортировка, агрегация, первый класс.
Все задачи — на материале детской футбольной лиги.

Как работать: пишешь код вместо `pass`, запускаешь  pytest -v test_tasks_02.py
Можно импортировать модули стандартной библиотеки (collections, functools и т. д.).
"""


# ─── Задача 1. Дубли команд ───────────────────────────────────────────
def unique_teams(names: list[str]) -> list[str]:
    """
    Тренеры вписывают названия команд как попало. Убрать дубли:
    - регистр не важен;
    - пробелы по краям и повторяющиеся пробелы внутри не важны;
    - в результат идёт ПЕРВОЕ встретившееся написание, но в «чистом» виде
      (без пробелов по краям, с одиночными пробелами внутри);
    - порядок — как в исходном списке.

    unique_teams(["Динамо Пресня", " динамо  пресня ", "Спартак", "СПАРТАК", "Торпедо"])
    -> ["Динамо Пресня", "Спартак", "Торпедо"]
    """
    unique_names_set = set(' '.join(name.lower().strip().split()) for name in names)
    unique_names = []
    for name in names:
        new_name = ' '.join(name.lower().strip().split())
        if new_name in unique_names_set:
            unique_names.append(' '.join(name.strip().split()))
            unique_names_set.remove(new_name)
    return unique_names


# ─── Задача 2. Расписание ─────────────────────────────────────────────
def sort_matches(matches: list[dict]) -> list[dict]:
    """
    Отсортировать матчи:
      1) по дате (строка "ГГГГ-ММ-ДД") — по возрастанию;
      2) при одинаковой дате — по стадиону по алфавиту;
      3) при одинаковых дате и стадионе — по названию домашней команды (home) по алфавиту.
    Исходный список НЕ изменять — вернуть новый.

    Матч выглядит так:
    {"date": "2027-01-10", "stadium": "Манеж ЦСКА", "home": "Динамо", "away": "Спартак"}
    """
    return sorted(matches, key=lambda m: (m["date"], m["stadium"], m["home"]))


# ─── Задача 3. Турнирная таблица ──────────────────────────────────────
def standings(matches: list[dict]) -> list[dict]:
    """
    По списку сыгранных матчей построить турнирную таблицу.
    Матч: {"home": "Динамо", "away": "Спартак", "home_goals": 2, "away_goals": 1}

    Очки: победа — 3, ничья — 1, поражение — 0.
    Для каждой команды вернуть словарь:
      {"team": ..., "played": ..., "wins": ..., "draws": ..., "losses": ...,
       "goals_for": ..., "goals_against": ..., "goal_diff": ..., "points": ...}

    Порядок строк:
      1) очки — по убыванию;
      2) разница мячей — по убыванию;
      3) забитые — по убыванию;
      4) название — по алфавиту.
    """
    stats = {}
    table = []
    for match in matches:
      for team, scored, conceded in [
          (match["home"], match["home_goals"], match["away_goals"]),
          (match["away"], match["away_goals"], match["home_goals"]),
      ]:
          if team not in stats:
              stats[team] = {
                  "played": 0, "wins": 0, "draws": 0, "losses": 0,
                  "goals_for": 0, "goals_against": 0, "goal_diff": 0, "points": 0,
              }
          stats[team]["played"] += 1
          stats[team]["goals_for"] += scored
          stats[team]["goals_against"] += conceded
          if scored > conceded:
              stats[team]["wins"] += 1
              stats[team]["points"] += 3
          elif scored == conceded:
              stats[team]["draws"] += 1
              stats[team]["points"] += 1
          else:
              stats[team]["losses"] += 1
    for team, value in stats.items():
        new_stats = {"team": team, **value, "goal_diff": value["goals_for"] - value["goals_against"]}
        table.append(new_stats)

    table.sort(key=lambda x: (-x["points"], -x["goal_diff"], -x["goals_for"], x["team"]))
    return table
        

# ─── Задача 4. Обновление данных ──────────────────────────────────────
def merge_by_id(old: list[dict], new: list[dict]) -> list[dict]:
    """
    Слить два списка записей по полю "id" (как при обновлении данных из API):
    - если запись с таким id уже есть в old — дополнить/перезаписать её поля полями из new;
    - если такого id нет — добавить запись в конец;
    - порядок: сначала записи old в их порядке, затем новые id в порядке new;
    - исходные списки и словари НЕ изменять.

    merge_by_id(
        [{"id": 1, "name": "Динамо", "active": True}, {"id": 2, "name": "Спартак"}],
        [{"id": 2, "active": False}, {"id": 3, "name": "Торпедо"}],
    ) -> [{"id": 1, "name": "Динамо", "active": True},
          {"id": 2, "name": "Спартак", "active": False},
          {"id": 3, "name": "Торпедо"}]
    """
    old_copy = copy.deepcopy(old)
    new_copy = copy.deepcopy(new)
    for new_record in new_copy:
        for old_record in old_copy:
            if new_record["id"] == old_record["id"]:
                old_record.update(new_record)
                break
        else:
            old_copy.append(new_record)
    return old_copy


# ─── Задача 5. Класс Match ────────────────────────────────────────────
class Match:
    """
    Матч с итоговым счётом.

    Match("Динамо", "Спартак", 2, 1)
    - Голы не могут быть отрицательными → ValueError.
    - Команда не может играть сама с собой (без учёта регистра) → ValueError.
    - Атрибуты: home, away, home_goals, away_goals, technical (по умолчанию False).

    Свойство winner -> название победителя или None при ничьей.

    Альтернативный конструктор (правило лиги: техническое поражение — 0:5):
      Match.technical_defeat("Динамо", "Спартак", loser="Динамо")
      -> матч Динамо 0:5 Спартак, technical=True.
      Если loser не одна из двух команд → ValueError.

    str(Match("Динамо", "Спартак", 2, 1))         -> "Динамо 2:1 Спартак"
    str(технического поражения)                   -> "Динамо 0:5 Спартак (ТП)"

    Два матча равны (==), если совпадают команды, счёт и флаг technical.
    """
    def __init__(self, home: str, away: str, home_goals: int, away_goals: int):
        if home_goals < 0 or away_goals < 0:
            raise ValueError ("Голы не могут быть отрицательными")
        if home.lower() == away.lower():
            raise ValueError ("Команда не может играть сама с собой")
        self.home = home
        self.away = away
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.technical = False

    @property
    def winner(self):
        if self.home_goals > self.away_goals:
            return self.home
        elif self.home_goals < self.away_goals:
            return self.away
        else:
            return None

    @classmethod
    def technical_defeat(cls, home: str, away: str, loser: str):
        if loser.lower() not in (home.lower(), away.lower()):
            raise ValueError ("Loser must be one of the teams")
        home_goals, away_goals = (0, 5) if loser.lower() == home.lower() else (5, 0)
        match = cls(home, away, home_goals, away_goals)
        match.technical = True
        return match

    def __str__(self):
        result = f"{self.home} {self.home_goals}:{self.away_goals} {self.away}"
        if self.technical:
            result += " (ТП)"
        return result

    def __eq__(self, other):
        if not isinstance(other, Match):
            return NotImplemented
        return (self.home.lower(), self.away.lower(), self.home_goals, self.away_goals, self.technical) == \
               (other.home.lower(), other.away.lower(), other.home_goals, other.away_goals, other.technical)

  

