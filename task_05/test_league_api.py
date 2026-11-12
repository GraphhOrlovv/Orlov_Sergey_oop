from unittest.mock import Mock, patch

import pytest

from league_api import (ApiError, LeagueClient, NotFoundError, SchemaError,
                        validate_team)

BASE = "https://api.test"


# ---------------- вспомогательное: фейковый ответ сервера ----------------

def fake_response(status=200, body=None, text=""):
    """Объект, похожий на requests.Response."""
    resp = Mock()
    resp.status_code = status
    resp.text = text
    if body is None:
        resp.json.side_effect = ValueError("No JSON")
    else:
        resp.json.return_value = body
    return resp


@pytest.fixture
def session():
    s = Mock()
    s.headers = {}
    s.request.return_value = fake_response(200, {})
    return s


@pytest.fixture
def client(session):
    return LeagueClient(BASE + "/", token="secret", session=session)


def sent(session):
    """Что ушло в session.request: (method, url, kwargs без позиционных)."""
    args, kwargs = session.request.call_args
    kwargs = dict(kwargs)
    method = args[0] if len(args) > 0 else kwargs.pop("method")
    url = args[1] if len(args) > 1 else kwargs.pop("url")
    return method, url, kwargs


# ------------------------- 1. исключения -------------------------

def test_api_error_fields_and_str():
    err = ApiError(404, "Команда не найдена")
    assert err.status_code == 404
    assert err.message == "Команда не найдена"
    assert str(err) == "404: Команда не найдена"
    assert isinstance(err, Exception)


def test_not_found_is_api_error():
    err = NotFoundError(404, "нет")
    assert isinstance(err, ApiError)
    assert err.status_code == 404
    assert str(err) == "404: нет"


def test_schema_error_is_separate():
    assert issubclass(SchemaError, Exception)
    assert not issubclass(SchemaError, ApiError)


# ------------------------- 2a. __init__ -------------------------

def test_init_strips_slash_and_sets_token(client, session):
    assert client.base_url == BASE
    assert client.timeout == 5
    assert client.session is session
    assert session.headers["Authorization"] == "Bearer secret"


def test_init_without_token_no_header(session):
    LeagueClient(BASE, session=session)
    assert "Authorization" not in session.headers


def test_init_creates_real_session_by_default():
    with patch("league_api.requests.Session") as session_cls:
        c = LeagueClient(BASE)
    session_cls.assert_called_once_with()
    assert c.session is session_cls.return_value


# ------------------------- 2b. _request -------------------------

@pytest.mark.parametrize("path", ["/teams/7", "teams/7"])
def test_request_builds_url_and_passes_timeout(client, session, path):
    session.request.return_value = fake_response(200, {"id": 7})
    assert client._request("GET", path) == {"id": 7}
    method, url, kwargs = sent(session)
    assert (method, url) == ("GET", f"{BASE}/teams/7")
    assert kwargs == {"timeout": 5}


def test_request_passes_extra_kwargs(client, session):
    client._request("GET", "/matches", params={"season": 2026})
    _, _, kwargs = sent(session)
    assert kwargs == {"timeout": 5, "params": {"season": 2026}}


def test_request_404_raises_not_found(client, session):
    session.request.return_value = fake_response(404, {"error": "Команда не найдена"})
    with pytest.raises(NotFoundError, match="404: Команда не найдена") as exc_info:
        client._request("GET", "/teams/999")
    assert exc_info.value.status_code == 404


@pytest.mark.parametrize("status", [400, 401, 403, 409, 500, 503])
def test_request_errors_raise_api_error(client, session, status):
    session.request.return_value = fake_response(status, {"error": "плохо"})
    with pytest.raises(ApiError) as exc_info:
        client._request("GET", "/x")
    err = exc_info.value
    assert type(err) is ApiError
    assert (err.status_code, err.message) == (status, "плохо")


def test_request_error_without_json_uses_text(client, session):
    session.request.return_value = fake_response(502, body=None, text="Bad Gateway")
    with pytest.raises(ApiError, match="502: Bad Gateway"):
        client._request("GET", "/x")


def test_request_error_json_without_error_key_uses_text(client, session):
    session.request.return_value = fake_response(500, {"detail": "x"}, text="oops")
    with pytest.raises(ApiError, match="500: oops"):
        client._request("GET", "/x")


def test_request_204_returns_none_without_json(client, session):
    resp = fake_response(204, {"should": "not be read"})
    session.request.return_value = resp
    assert client._request("DELETE", "/matches/1") is None
    resp.json.assert_not_called()


def test_request_201_returns_json(client, session):
    session.request.return_value = fake_response(201, {"id": 5})
    assert client._request("POST", "/matches") == {"id": 5}


# ------------------------- 3. методы API -------------------------

def test_get_team(client, session):
    session.request.return_value = fake_response(200, {"id": 7, "name": "Динамо"})
    assert client.get_team(7) == {"id": 7, "name": "Динамо"}
    method, url, _ = sent(session)
    assert (method, url) == ("GET", f"{BASE}/teams/7")


def test_get_team_not_found(client, session):
    session.request.return_value = fake_response(404, {"error": "нет"})
    with pytest.raises(NotFoundError):
        client.get_team(999)


def test_list_matches_with_status(client, session):
    session.request.return_value = fake_response(200, [{"id": 1}, {"id": 2}])
    assert client.list_matches(2026, status="finished") == [{"id": 1}, {"id": 2}]
    method, url, kwargs = sent(session)
    assert (method, url) == ("GET", f"{BASE}/matches")
    assert kwargs["params"] == {"season": 2026, "status": "finished"}


def test_list_matches_without_status(client, session):
    session.request.return_value = fake_response(200, [])
    assert client.list_matches(2025) == []
    _, _, kwargs = sent(session)
    assert kwargs["params"] == {"season": 2025}


def test_create_match(client, session):
    session.request.return_value = fake_response(201, {"id": 10, "home_id": 1})
    assert client.create_match(1, 2, "2026-11-15") == {"id": 10, "home_id": 1}
    method, url, kwargs = sent(session)
    assert (method, url) == ("POST", f"{BASE}/matches")
    assert kwargs["json"] == {"home_id": 1, "away_id": 2, "date": "2026-11-15"}


def test_create_match_same_team_no_request(client, session):
    with pytest.raises(ValueError):
        client.create_match(3, 3, "2026-11-15")
    session.request.assert_not_called()


def test_delete_match(client, session):
    session.request.return_value = fake_response(204)
    assert client.delete_match(10) is None
    method, url, _ = sent(session)
    assert (method, url) == ("DELETE", f"{BASE}/matches/10")


# ------------------------- 4. validate_team -------------------------

def good_team():
    return {
        "id": 7,
        "name": "Динамо",
        "city": "Москва",
        "players": [{"name": "Петров", "number": 10}, {"name": "Иванов", "number": 1}],
        "founded": 1923,
    }


def test_validate_team_ok():
    data = good_team()
    assert validate_team(data) is data


def test_validate_team_empty_players_ok():
    data = good_team()
    data["players"] = []
    assert validate_team(data) is data


@pytest.mark.parametrize("field", ["id", "name", "city", "players"])
def test_validate_team_missing_field(field):
    data = good_team()
    del data[field]
    with pytest.raises(SchemaError, match=field):
        validate_team(data)


@pytest.mark.parametrize("field, value", [
    ("id", "7"),
    ("id", 0),
    ("id", -1),
    ("id", True),
    ("name", ""),
    ("name", "   "),
    ("name", 123),
    ("city", None),
    ("players", "Петров"),
    ("players", None),
])
def test_validate_team_bad_top_level(field, value):
    data = good_team()
    data[field] = value
    with pytest.raises(SchemaError, match=field):
        validate_team(data)


@pytest.mark.parametrize("player, field", [
    ({"number": 10}, "name"),
    ({"name": 5, "number": 10}, "name"),
    ({"name": "Петров"}, "number"),
    ({"name": "Петров", "number": "10"}, "number"),
    ({"name": "Петров", "number": 0}, "number"),
    ({"name": "Петров", "number": 100}, "number"),
    ({"name": "Петров", "number": False}, "number"),
])
def test_validate_team_bad_player(player, field):
    data = good_team()
    data["players"].append(player)
    with pytest.raises(SchemaError, match=field):
        validate_team(data)


def test_validate_team_player_not_dict():
    data = good_team()
    data["players"].append("Сидоров")
    with pytest.raises(SchemaError):
        validate_team(data)


def test_validate_team_duplicate_numbers():
    data = good_team()
    data["players"].append({"name": "Сидоров", "number": 10})
    with pytest.raises(SchemaError, match="number"):
        validate_team(data)


def test_validate_team_not_dict():
    with pytest.raises(SchemaError):
        validate_team([good_team()])


# ------------------- всё вместе: клиент + валидатор -------------------

def test_get_team_and_validate(client, session):
    session.request.return_value = fake_response(200, good_team())
    team = validate_team(client.get_team(7))
    assert team["name"] == "Динамо"
