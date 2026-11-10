import pytest

from tasks_04 import count_calls, memoize, require_role, retry


class User:
    def __init__(self, role):
        self.role = role


# ------------------------- 1. count_calls -------------------------

def test_count_calls_counts():
    @count_calls
    def goal(player):
        return f"Гол! {player}"

    assert goal.calls == 0
    assert goal("Петров") == "Гол! Петров"
    goal("Иванов")
    goal(player="Сидоров")
    assert goal.calls == 3


def test_count_calls_separate_counters():
    @count_calls
    def a():
        pass

    @count_calls
    def b():
        pass

    a(); a(); b()
    assert (a.calls, b.calls) == (2, 1)


def test_count_calls_keeps_name_and_doc():
    @count_calls
    def goal():
        """Забить гол."""

    assert goal.__name__ == "goal"
    assert goal.__doc__ == "Забить гол."


# ------------------------- 2. require_role -------------------------

@pytest.fixture
def publish():
    @require_role("admin", "coach")
    def publish_result(user, match_id, score):
        """Опубликовать счёт."""
        return f"{match_id}: {score}"

    return publish_result


@pytest.mark.parametrize("role", ["admin", "coach"])
def test_require_role_allowed(publish, role):
    assert publish(User(role), 7, score="2:1") == "7: 2:1"


@pytest.mark.parametrize("role", ["viewer", "player", ""])
def test_require_role_denied(publish, role):
    with pytest.raises(PermissionError, match=f"Роль '{role}' не может выполнить publish_result"):
        publish(User(role), 7, "2:1")


def test_require_role_does_not_call_func_when_denied():
    called = []

    @require_role("admin")
    def delete_team(user, team_id):
        called.append(team_id)

    with pytest.raises(PermissionError):
        delete_team(User("coach"), 1)
    assert called == []


def test_require_role_keeps_name_and_doc(publish):
    assert publish.__name__ == "publish_result"
    assert publish.__doc__ == "Опубликовать счёт."


# ------------------------- 3. retry -------------------------

def make_flaky(fails, exc=ConnectionError):
    """Функция, которая падает fails раз, потом возвращает 'таблица'."""
    attempts = []

    def get_table():
        """Получить таблицу."""
        attempts.append(1)
        if len(attempts) <= fails:
            raise exc(f"попытка {len(attempts)}")
        return "таблица"

    return get_table, attempts


def test_retry_succeeds_after_failures():
    func, attempts = make_flaky(fails=2)
    wrapped = retry(times=3, exceptions=(ConnectionError,))(func)
    assert wrapped() == "таблица"
    assert len(attempts) == 3


def test_retry_success_first_time_no_extra_calls():
    func, attempts = make_flaky(fails=0)
    assert retry(times=5)(func)() == "таблица"
    assert len(attempts) == 1


def test_retry_raises_last_error():
    func, attempts = make_flaky(fails=10)
    wrapped = retry(times=3, exceptions=(ConnectionError,))(func)
    with pytest.raises(ConnectionError, match="попытка 3"):
        wrapped()
    assert len(attempts) == 3


def test_retry_other_exception_not_retried():
    func, attempts = make_flaky(fails=10, exc=KeyError)
    wrapped = retry(times=3, exceptions=(ConnectionError,))(func)
    with pytest.raises(KeyError):
        wrapped()
    assert len(attempts) == 1


def test_retry_defaults():
    func, attempts = make_flaky(fails=2, exc=ValueError)
    assert retry()(func)() == "таблица"
    assert len(attempts) == 3


def test_retry_passes_arguments():
    @retry(times=2)
    def add(a, b=0):
        return a + b

    assert add(2, b=3) == 5


@pytest.mark.parametrize("times", [0, -1])
def test_retry_invalid_times(times):
    with pytest.raises(ValueError):
        retry(times=times)


def test_retry_keeps_name_and_doc():
    func, _ = make_flaky(fails=0)
    wrapped = retry()(func)
    assert wrapped.__name__ == "get_table"
    assert wrapped.__doc__ == "Получить таблицу."


# ------------------------- 4. memoize -------------------------

@pytest.fixture
def rating():
    calls = []

    @memoize
    def team_rating(team_id, season=2026):
        """Рейтинг команды."""
        calls.append((team_id, season))
        return team_id * 10 + season % 10

    return team_rating, calls


def test_memoize_caches(rating):
    func, calls = rating
    assert func(1) == 16
    assert func(1) == 16
    assert func(2) == 26
    assert calls == [(1, 2026), (2, 2026)]
    assert func.hits == 1


def test_memoize_different_args_different_entries(rating):
    func, calls = rating
    func(1, 2025)
    func(1, 2026)
    func(1, 2025)
    assert len(calls) == 2
    assert func.hits == 1


def test_memoize_clear(rating):
    func, calls = rating
    func(1); func(1)
    func.clear()
    assert func.hits == 0
    func(1)
    assert len(calls) == 2


def test_memoize_caches_none_result():
    calls = []

    @memoize
    def find(x):
        calls.append(x)
        return None

    find(1); find(1)
    assert calls == [1]
    assert find.hits == 1


def test_memoize_keeps_name_and_doc(rating):
    func, _ = rating
    assert func.__name__ == "team_rating"
    assert func.__doc__ == "Рейтинг команды."
