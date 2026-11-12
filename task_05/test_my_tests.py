"""
Задача 5. Теперь ты — автотестер. Напиши тесты сам.

Это то, что делают на работе: клиент уже есть (твой league_api.py),
сервера нет, а проверить поведение нужно. Готовые тесты в
test_league_api.py НЕ подглядывать до того, как напишешь свои :)

Инструменты:
    from unittest.mock import Mock, patch

    resp = Mock()
    resp.status_code = 200
    resp.json.return_value = {...}         # что вернёт resp.json()
    resp.json.side_effect = ValueError()   # resp.json() бросит ошибку

    session = Mock()
    session.headers = {}
    session.request.return_value = resp    # что вернёт session.request(...)

    session.request.assert_called_once()   # был ли ровно один вызов
    session.request.assert_not_called()    # не было ни одного
    args, kwargs = session.request.call_args   # с чем вызвали

Требования:
  * общие вещи (session, client) вынести в фикстуры;
  * хотя бы один тест через @pytest.mark.parametrize;
  * каждый тест проверяет ОДНО поведение и назван так, чтобы
    по имени было понятно, что сломалось.

Запуск: pytest -v test_my_tests.py
"""

import json

import pytest
from unittest.mock import Mock

from league_api import ApiError, LeagueClient, NotFoundError, SchemaError, validate_team

BASE_URL = "https://api.test"

def fake_response(status=200, body=None, text=""):
    resp=Mock()
    resp.status_code = status
    resp.text = text
    if body is None:
        resp.json.side_effect = ValueError("Нет json")
    else:
        resp.json.return_value = body
    return resp
    

# TODO: фикстура session
@pytest.fixture
def session():
    session = Mock()
    session.headers = {}
    session.request.return_value = fake_response(200, {})
    return session

# TODO: фикстура client
@pytest.fixture
def client(session):
    return LeagueClient(base_url=BASE_URL + "/", token="secret", session=session)

# 5.1 get_team возвращает JSON из ответа и стучится на правильный URL
def test_get_team_returns_json_and_calls_correct_url(session, client):
    expected = {"id": 7, "name": "Динамо"}
    session.request.return_value = fake_response(200, expected)

    team = client.get_team(7)

    assert team == expected
    session.request.assert_called_once_with("GET", f"{BASE_URL}/teams/7", timeout=5)

# 5.2 при 404 get_team бросает NotFoundError, и в ней правильный status_code
def test_status_404_get_team(session, client):
    session.request.return_value = fake_response(404, text="Not Found")
    with pytest.raises(NotFoundError, match="404: Not Found") as exc_info:
        client.get_team(1000)

    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "Not Found"

# 5.3 параметризованный: коды 400, 403, 500 -> ApiError с текстом из поля "error"
@pytest.mark.parametrize(
    "status", [400, 403, 500]
    )
def test_get_team_error_codes_raise_api_error_with_message(session, client, status):
    session.request.return_value = fake_response(status, {"error": "Ошибка"})
    with pytest.raises(ApiError) as exc_info:
        client.get_team(1000)
    
    assert exc_info.value.status_code == status
    assert exc_info.value.message == "Ошибка"
    assert exc_info.type is ApiError

# 5.4 create_match с одинаковыми командами -> ValueError и запрос НЕ ушёл
def test_create_match_with_equal_teams_raise_value_error_and_no_request(session, client):
    with pytest.raises(ValueError):
        client.create_match(home_id="3", away_id="3", date="2026-11-15")

    session.request.assert_not_called()


# 5.5 list_matches без status -> в params нет ключа "status"
def test_list_maches_without_status(session, client):
    session.request.return_value = fake_response(200, [{"id": 1}, {"id": 2}])

    matches = client.list_matches(season=2026)
    _, kwargs = session.request.call_args
    assert kwargs["params"] == {"season": 2026}
    assert matches == [{"id": 1}, {"id": 2}]

# 5.6 validate_team: хорошая команда проходит, команда без "name" -> SchemaError
def good_team():
    return {
        "id": 5,
        "name": "Спартак",
        "city": "Москва",
        "players": [{"name": "Иванов", "number": 10}, {"name": "Сидоров", "number": 12}],
        "founded": 2015,
    }

def bad_team():
    return {
        "id": 5,
        "name": "Спартак",
        "city": "Москва",
        "players": [{"name": "Иванов", "number": '10'}, {"name": "Сидоров", "number": 12}],
        "founded": 2015,
    }

def test_validate_team_ok():
    data = good_team()
    assert validate_team(data) is data

def test_validate_team_without_name_raises_schema_error():
    data = good_team()
    del data["name"]
    with pytest.raises(SchemaError, match="name"):
        validate_team(data)
    

# 5.7 (со звёздочкой) клиент + валидатор вместе: сервер вернул 200, но в JSON
#     у игрока номер "10" строкой -> validate_team(client.get_team(...)) падает
#     со SchemaError. Это реальный кейс: API «зелёный», а данные битые.
def test_get_team_200_with_string_number_fails_validation(session, client):
    session.request.return_value = fake_response(200, bad_team())

    team = client.get_team(5)

    with pytest.raises(SchemaError, match="number"):
        validate_team(team)
    