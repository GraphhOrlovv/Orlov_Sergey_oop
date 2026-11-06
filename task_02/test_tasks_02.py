import copy
import pytest
from tasks_02 import unique_teams, sort_matches, standings, merge_by_id, Match


# ─── 1. Дубли команд ──────────────────────────────────────────────────
def test_unique_teams_example():
    names = ["Динамо Пресня", " динамо  пресня ", "Спартак", "СПАРТАК", "Торпедо"]
    assert unique_teams(names) == ["Динамо Пресня", "Спартак", "Торпедо"]


def test_unique_teams_cleans_first_spelling():
    assert unique_teams(["  Динамо   Жулебино ", "динамо жулебино"]) == ["Динамо Жулебино"]


def test_unique_teams_different_teams_kept():
    assert unique_teams(["Динамо Пресня", "Динамо Жулебино"]) == ["Динамо Пресня", "Динамо Жулебино"]


def test_unique_teams_empty():
    assert unique_teams([]) == []


# ─── 2. Расписание ────────────────────────────────────────────────────
M = [
    {"date": "2027-01-17", "stadium": "Манеж ЦСКА", "home": "Динамо", "away": "Спартак"},
    {"date": "2027-01-10", "stadium": "Лужники", "home": "Торпедо", "away": "Локомотив"},
    {"date": "2027-01-10", "stadium": "Лужники", "home": "Арсенал", "away": "Динамо"},
    {"date": "2027-01-10", "stadium": "Варяг", "home": "Спартак", "away": "Торпедо"},
]


def test_sort_matches_order():
    result = sort_matches(M)
    assert [(m["date"], m["stadium"], m["home"]) for m in result] == [
        ("2027-01-10", "Варяг", "Спартак"),
        ("2027-01-10", "Лужники", "Арсенал"),
        ("2027-01-10", "Лужники", "Торпедо"),
        ("2027-01-17", "Манеж ЦСКА", "Динамо"),
    ]


def test_sort_matches_does_not_modify_input():
    original = copy.deepcopy(M)
    result = sort_matches(M)
    assert isinstance(result, list)
    assert M == original


def test_sort_matches_returns_new_list():
    result = sort_matches(M)
    assert isinstance(result, list) and result is not M


# ─── 3. Турнирная таблица ─────────────────────────────────────────────
GAMES = [
    {"home": "Динамо", "away": "Спартак", "home_goals": 2, "away_goals": 1},
    {"home": "Торпедо", "away": "Динамо", "home_goals": 0, "away_goals": 0},
    {"home": "Спартак", "away": "Торпедо", "home_goals": 3, "away_goals": 0},
    {"home": "Динамо", "away": "Торпедо", "home_goals": 0, "away_goals": 5},
]


def test_standings_order():
    assert [row["team"] for row in standings(GAMES)] == ["Торпедо", "Динамо", "Спартак"]


def test_standings_row_content():
    table = {row["team"]: row for row in standings(GAMES)}
    assert table["Динамо"] == {
        "team": "Динамо", "played": 3, "wins": 1, "draws": 1, "losses": 1,
        "goals_for": 2, "goals_against": 6, "goal_diff": -4, "points": 4,
    }
    assert table["Торпедо"]["points"] == 4
    assert table["Торпедо"]["goal_diff"] == 2
    assert table["Спартак"]["points"] == 3


def test_standings_tie_by_name():
    games = [{"home": "Б", "away": "А", "home_goals": 1, "away_goals": 1}]
    assert [row["team"] for row in standings(games)] == ["А", "Б"]


def test_standings_tie_by_goals_for():
    # X и Y: по 3 очка и разница +1, но X забил больше
    games = [
        {"home": "X", "away": "Z", "home_goals": 3, "away_goals": 2},
        {"home": "Y", "away": "W", "home_goals": 1, "away_goals": 0},
    ]
    assert [row["team"] for row in standings(games)] == ["X", "Y", "Z", "W"]


def test_standings_empty():
    assert standings([]) == []


# ─── 4. Слияние по id ─────────────────────────────────────────────────
def test_merge_by_id_example():
    old = [{"id": 1, "name": "Динамо", "active": True}, {"id": 2, "name": "Спартак"}]
    new = [{"id": 2, "active": False}, {"id": 3, "name": "Торпедо"}]
    assert merge_by_id(old, new) == [
        {"id": 1, "name": "Динамо", "active": True},
        {"id": 2, "name": "Спартак", "active": False},
        {"id": 3, "name": "Торпедо"},
    ]


def test_merge_by_id_overwrites_fields():
    assert merge_by_id([{"id": 1, "name": "Old"}], [{"id": 1, "name": "New"}]) == [{"id": 1, "name": "New"}]


def test_merge_by_id_does_not_modify_input():
    old = [{"id": 1, "name": "Динамо"}]
    new = [{"id": 1, "name": "Спартак"}]
    old_copy, new_copy = copy.deepcopy(old), copy.deepcopy(new)
    assert merge_by_id(old, new) == [{"id": 1, "name": "Спартак"}]
    assert old == old_copy and new == new_copy


def test_merge_by_id_empty():
    assert merge_by_id([], []) == []
    assert merge_by_id([], [{"id": 5}]) == [{"id": 5}]


# ─── 5. Класс Match ───────────────────────────────────────────────────
def test_match_attributes():
    m = Match("Динамо", "Спартак", 2, 1)
    assert (m.home, m.away, m.home_goals, m.away_goals, m.technical) == ("Динамо", "Спартак", 2, 1, False)


@pytest.mark.parametrize("home_goals, away_goals, winner", [(2, 1, "Динамо"), (0, 3, "Спартак"), (1, 1, None)])
def test_match_winner(home_goals, away_goals, winner):
    assert Match("Динамо", "Спартак", home_goals, away_goals).winner == winner


def test_match_str():
    assert str(Match("Динамо", "Спартак", 2, 1)) == "Динамо 2:1 Спартак"


@pytest.mark.parametrize("hg, ag", [(-1, 0), (0, -2)])
def test_match_negative_goals(hg, ag):
    with pytest.raises(ValueError):
        Match("Динамо", "Спартак", hg, ag)


def test_match_same_team():
    with pytest.raises(ValueError):
        Match("Динамо", "динамо", 1, 0)


@pytest.mark.parametrize("loser, score", [("Динамо", (0, 5)), ("Спартак", (5, 0))])
def test_match_technical_defeat(loser, score):
    m = Match.technical_defeat("Динамо", "Спартак", loser=loser)
    assert (m.home_goals, m.away_goals) == score
    assert m.technical is True
    assert m.winner == ("Спартак" if loser == "Динамо" else "Динамо")


def test_match_technical_str():
    assert str(Match.technical_defeat("Динамо", "Спартак", loser="Динамо")) == "Динамо 0:5 Спартак (ТП)"


def test_match_technical_wrong_loser():
    with pytest.raises(ValueError):
        Match.technical_defeat("Динамо", "Спартак", loser="Торпедо")


def test_match_equality():
    assert Match("Динамо", "Спартак", 2, 1) == Match("Динамо", "Спартак", 2, 1)
    assert Match("Динамо", "Спартак", 2, 1) != Match("Динамо", "Спартак", 1, 2)
    assert Match("Динамо", "Спартак", 0, 5) != Match.technical_defeat("Динамо", "Спартак", loser="Динамо")
