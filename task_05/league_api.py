"""
Набор 05. API-клиент лиги на requests + свои исключения + проверка JSON.

Реального сервера НЕТ и не нужно: тесты подменяют сетевой слой моками.
Для этого клиент принимает объект session снаружи (это называется
«внедрение зависимости»). В бою туда идёт requests.Session(),
в тестах — Mock, который возвращает заранее заготовленный ответ.

Перед началом:  pip install requests
Запуск:         pytest -v test_league_api.py
Одна задача:    pytest -v test_league_api.py -k request

Как устроен API лиги (выдуманный):
    GET    /teams/{id}                 -> {"id": 7, "name": "Динамо", ...}
    GET    /matches?season=2026&status=finished -> [{...}, {...}]
    POST   /matches   json={"home_id": 1, "away_id": 2, "date": "2026-11-15"}
                                       -> 201 + созданный матч
    DELETE /matches/{id}               -> 204, тела нет
Ошибки сервер отдаёт так:  код 4xx/5xx и тело {"error": "текст"}.
"""

import requests


# ---------------------------------------------------------------------------
# Задача 1. Свои исключения
# ---------------------------------------------------------------------------
# ApiError(status_code, message)
#   * наследник Exception;
#   * хранит атрибуты .status_code и .message;
#   * str(err) -> "404: Команда не найдена"
#
# NotFoundError — наследник ApiError (для кода 404). Своего кода не нужно,
#   достаточно правильно унаследоваться.
#
# SchemaError — наследник Exception, бросается валидатором в задаче 4,
#   когда JSON пришёл, но не той структуры.

class ApiError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"{status_code}: {message}")
        self.status_code = status_code
        self.message = message


class NotFoundError(ApiError):
    pass


class SchemaError(Exception):
    pass


# ---------------------------------------------------------------------------
# Задачи 2–3. Клиент
# ---------------------------------------------------------------------------

class LeagueClient:
    def __init__(self, base_url, token=None, timeout=5, session=None):
        """
        Задача 2a.
          * base_url хранить БЕЗ слеша на конце: "https://api.test/" -> "https://api.test"
          * self.timeout = timeout
          * self.session = переданная session, а если её нет — requests.Session()
          * если передан token — добавить в заголовки сессии
                Authorization: Bearer <token>
            (у сессии есть словарь self.session.headers)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        if session:
            self.session = session
        else:
            self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _request(self, method, path, **kwargs):
        """
        Задача 2b. Единая точка для всех запросов.
          * url = base_url + "/" + path без ведущего слеша
                ("/teams/7" и "teams/7" -> "https://api.test/teams/7")
          * вызвать ровно так:
                self.session.request(method, url, timeout=self.timeout, **kwargs)
          * код 404        -> NotFoundError
          * код >= 400     -> ApiError
                message: поле "error" из JSON-тела; если тело не JSON
                (response.json() бросает ValueError) или поля нет —
                взять response.text
          * код 204        -> вернуть None (тела нет, .json() не вызывать)
          * иначе          -> вернуть response.json()
        """
        url = self.base_url + "/" + path.lstrip("/")
        resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        
        if resp.status_code >= 400:
            try:
                message = resp.json()["error"]
            except (ValueError, KeyError, TypeError):
                message = resp.text
            if resp.status_code == 404:
                raise NotFoundError(resp.status_code, message)
            raise ApiError(resp.status_code, message)
        if resp.status_code == 204:
            return None
        return resp.json()

    # --- Задача 3. Методы API. Каждый — одна-две строки через _request ---

    def get_team(self, team_id):
        """GET /teams/{team_id} -> dict."""
        return self._request("GET", f'/teams/{team_id}')

    def list_matches(self, season, status=None):
        """
        GET /matches с query-параметрами через params=...
          * season передаётся всегда;
          * status — только если он не None (не слать "status": None).
        """
        params = {"season": season}
        if status is not None:
            params["status"] = status
        return self._request("GET", '/matches', params=params)

    def create_match(self, home_id, away_id, date):
        """
        POST /matches, тело через json={"home_id":..., "away_id":..., "date":...}
          * если home_id == away_id -> ValueError, и запрос НЕ отправлять.
        """
        if home_id == away_id:
            raise ValueError("Команда не может играть сама с собой")
        body = {"home_id": home_id, 
                "away_id": away_id, 
                "date": date}
        return self._request("POST", '/matches', json=body)

    def delete_match(self, match_id):
        """DELETE /matches/{match_id} -> None."""
        return self._request("DELETE", f'/matches/{match_id}')


# ---------------------------------------------------------------------------
# Задача 4. Проверка структуры ответа
# ---------------------------------------------------------------------------
# validate_team(data) — проверяет JSON команды и возвращает его же,
# если всё в порядке. Иначе SchemaError, в тексте которого есть ИМЯ поля.
#
# Ожидаемая структура:
#   {
#     "id": 7,                       int, > 0  (bool не считается int!)
#     "name": "Динамо",              str, не пустая (пробелы не в счёт)
#     "city": "Москва",              str
#     "players": [                   list (может быть пустым)
#         {"name": "Петров", "number": 10},   name: str, number: int 1..99
#     ]
#   }
# Лишние поля — не ошибка.
# Номера игроков внутри команды не должны повторяться -> SchemaError ("number").
#
# Подсказка: isinstance(True, int) == True — поэтому bool надо отсечь отдельно.

def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)

def validate_team(data):
    numbers_set = set()
    if not isinstance(data, dict):
        raise SchemaError("Данные не в формате json!")
    for field in ("id", "name", "city", "players"):
        if field not in data:
            raise SchemaError(f"Отсутствует поле {field!r}")
    if not _is_int(data["id"]) or data["id"] <= 0:
        raise SchemaError("id")
    elif not isinstance(data["name"], str) or not data["name"].strip():
        raise SchemaError("name")
    elif not isinstance(data["city"], str) or not data["city"]:
        raise SchemaError("city")
    elif not isinstance(data["players"], list):
        raise SchemaError(f"players: {data['players']} не является списком")
    for player in data["players"]:
        for field_player in ("name", "number"):
            if field_player not in player:
                raise SchemaError(f"Отсутствует поле {field_player!r}")
        if not isinstance(player, dict):
            raise SchemaError(f"{player} не является словарём")
        if not isinstance(player["name"], str) or not player["name"].strip():
            raise SchemaError("name")
        if not _is_int(player["number"]) or player["number"] not in range(1, 100):
            raise SchemaError("number")
        if player["number"] in numbers_set:
            raise SchemaError("number")
        numbers_set.add(player["number"])
    return data

