import pytest
from tasks_01 import is_palindrome, word_count, group_by_status, diff_ids, flatten


# ─── 1. Палиндром ─────────────────────────────────────────────────────
@pytest.mark.parametrize("text, expected", [
    ("А роза упала на лапу Азора", True),
    ("Madam, I'm Adam", True),
    ("Python", False),
    ("", True),
    ("a", True),
    ("ab", False),
    ("12321", True),
    ("Казак!", True),
])
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected


# ─── 2. Частота слов ──────────────────────────────────────────────────
def test_word_count_basic():
    assert word_count("Тест, тест! И ещё   тест.") == {"тест": 3, "и": 1, "ещё": 1}


def test_word_count_empty():
    assert word_count("") == {}


def test_word_count_only_spaces():
    assert word_count("   ") == {}


def test_word_count_punctuation():
    assert word_count("Да? Да! Нет: да;") == {"да": 3, "нет": 1}


# ─── 3. Группировка ───────────────────────────────────────────────────
def test_group_by_status():
    data = [
        {"url": "/users", "status": 200},
        {"url": "/teams", "status": 500},
        {"url": "/games", "status": 200},
    ]
    assert group_by_status(data) == {200: ["/users", "/games"], 500: ["/teams"]}


def test_group_by_status_empty():
    assert group_by_status([]) == {}


def test_group_by_status_keeps_order():
    data = [{"url": f"/p{i}", "status": 404} for i in range(5)]
    assert group_by_status(data) == {404: ["/p0", "/p1", "/p2", "/p3", "/p4"]}


# ─── 4. Сравнение id ──────────────────────────────────────────────────
def test_diff_ids():
    assert diff_ids([1, 2, 3, 4], [2, 4, 5, 5]) == {"missing": [1, 3], "extra": [5]}


def test_diff_ids_equal():
    assert diff_ids([3, 1, 2], [1, 2, 3]) == {"missing": [], "extra": []}


def test_diff_ids_sorted_unique():
    assert diff_ids([9, 9, 1], []) == {"missing": [1, 9], "extra": []}


# ─── 5. Плоский словарь ───────────────────────────────────────────────
def test_flatten():
    data = {"user": {"name": "Ann", "address": {"city": "Москва"}}, "id": 1}
    assert flatten(data) == {"user.name": "Ann", "user.address.city": "Москва", "id": 1}


def test_flatten_already_flat():
    assert flatten({"a": 1, "b": [1, 2]}) == {"a": 1, "b": [1, 2]}


def test_flatten_deep():
    assert flatten({"a": {"b": {"c": {"d": 0}}}}) == {"a.b.c.d": 0}


def test_flatten_empty():
    assert flatten({}) == {}
