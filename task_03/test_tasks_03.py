from datetime import date, timedelta
import pytest
from tasks_03 import Player, Team, Season, Stage, Championship, PlayoffCup, RoundRobinCup, User


# ═══ 1. Player ════════════════════════════════════════════════════════
def test_player_name_cleaned():
    assert Player("  Иванов   Иван ", date(2016, 5, 3)).name == "Иванов Иван"


@pytest.mark.parametrize("name", ["", "   "])
def test_player_empty_name(name):
    with pytest.raises(ValueError):
        Player(name, date(2016, 5, 3))


def test_player_future_birth_date():
    with pytest.raises(ValueError):
        Player("Иванов Иван", date.today() + timedelta(days=1))


@pytest.mark.parametrize("day, expected", [
    (date(2026, 5, 2), 9),    # накануне дня рождения
    (date(2026, 5, 3), 10),   # в день рождения
    (date(2026, 12, 31), 10),
    (date(2016, 5, 3), 0),
])
def test_player_age_on(day, expected):
    assert Player("Иванов Иван", date(2016, 5, 3)).age_on(day) == expected


def test_player_birth_year():
    assert Player("Иванов Иван", date(2016, 5, 3)).birth_year == 2016


@pytest.mark.parametrize("division, expected", [(2016, True), (2015, True), (2017, False)])
def test_player_can_play_in(division, expected):
    assert Player("Иванов Иван", date(2016, 5, 3)).can_play_in(division) is expected


def test_player_from_string():
    p = Player.from_string("Петров Пётр;2017-09-01")
    assert (p.name, p.birth_date) == ("Петров Пётр", date(2017, 9, 1))


@pytest.mark.parametrize("raw", ["Петров Пётр", "Петров Пётр;01.09.2017", "Петров;2017-02-30", ";2017-09-01"])
def test_player_from_string_bad(raw):
    with pytest.raises(ValueError):
        Player.from_string(raw)


def test_player_repr():
    assert repr(Player("Иванов Иван", date(2016, 5, 3))) == "Player('Иванов Иван', date(2016, 5, 3))"


def test_player_equality_and_hash():
    a = Player("Иванов Иван", date(2016, 5, 3))
    b = Player("иванов иван", date(2016, 5, 3))
    c = Player("Иванов Иван", date(2016, 5, 4))
    assert a == b and a != c
    assert len({a, b, c}) == 2


# ═══ 2. Team ══════════════════════════════════════════════════════════
@pytest.fixture
def players():
    return [
        Player("Иванов Иван", date(2016, 5, 3)),
        Player("Петров Пётр", date(2017, 9, 1)),
        Player("Сидоров Олег", date(2015, 1, 20)),
    ]


@pytest.fixture
def team(players):
    t = Team("Динамо Пресня")
    for p in players:
        t.add(p)
    return t


def test_team_len_and_str(team):
    assert len(team) == 3
    assert str(team) == "Динамо Пресня (3 игр.)"


def test_team_empty():
    t = Team("Спартак")
    assert len(t) == 0 and t.youngest() is None


def test_team_contains(team, players):
    assert players[0] in team
    assert "ПЕТРОВ ПЁТР" in team
    assert "Кузнецов" not in team
    assert Player("Кузнецов Ян", date(2016, 1, 1)) not in team


def test_team_iter_and_getitem(team, players):
    assert list(team) == players
    assert team[1] == players[1]


def test_team_add_duplicate(team):
    with pytest.raises(ValueError):
        team.add(Player("иванов иван", date(2016, 5, 3)))


def test_team_max_players():
    t = Team("Торпедо")
    for i in range(Team.MAX_PLAYERS):
        t.add(Player(f"Игрок {i}", date(2016, 1, 1)))
    with pytest.raises(ValueError):
        t.add(Player("Лишний Игрок", date(2016, 1, 1)))


def test_team_max_players_is_class_attribute():
    assert "MAX_PLAYERS" in vars(Team)


def test_team_remove(team):
    team.remove("петров пётр")
    assert len(team) == 2 and "Петров Пётр" not in team
    with pytest.raises(KeyError):
        team.remove("Петров Пётр")


def test_team_youngest(team):
    assert team.youngest().name == "Петров Пётр"


def test_teams_do_not_share_players():
    a, b = Team("А"), Team("Б")
    a.add(Player("Иванов Иван", date(2016, 5, 3)))
    assert len(b) == 0


# ═══ 3. Season ════════════════════════════════════════════════════════
@pytest.fixture
def winter():
    return Season("Зима 2027", date(2027, 1, 10), date(2027, 3, 28))


@pytest.mark.parametrize("day, status", [
    (date(2027, 1, 9), "Запланирован"),
    (date(2027, 1, 10), "Идёт"),
    (date(2027, 2, 15), "Идёт"),
    (date(2027, 3, 28), "Идёт"),
    (date(2027, 3, 29), "Завершён"),
])
def test_season_status(winter, day, status):
    assert winter.status_on(day) == status


def test_season_contains(winter):
    assert date(2027, 1, 10) in winter
    assert date(2027, 3, 28) in winter
    assert date(2027, 4, 1) not in winter


def test_season_len():
    assert len(Season("Тест", date(2027, 1, 10), date(2027, 1, 12))) == 3
    assert len(Season("Один день", date(2027, 1, 10), date(2027, 1, 10))) == 1


def test_season_validation():
    with pytest.raises(ValueError):
        Season("", date(2027, 1, 10), date(2027, 3, 28))
    with pytest.raises(ValueError):
        Season("Зима", date(2027, 3, 28), date(2027, 1, 10))


def test_season_sorting(winter):
    autumn = Season("Осень 2026", date(2026, 9, 5), date(2026, 12, 20))
    spring = Season("Весна 2027", date(2027, 4, 3), date(2027, 6, 1))
    assert [s.name for s in sorted([spring, winter, autumn])] == ["Осень 2026", "Зима 2027", "Весна 2027"]
    assert autumn < winter and spring > winter and winter >= winter


def test_season_equality(winter):
    assert winter == Season("Зима 2027", date(2027, 1, 10), date(2027, 3, 28))
    assert winter != Season("Зима 2027", date(2027, 1, 10), date(2027, 3, 29))


# ═══ 4. Stage ═════════════════════════════════════════════════════════
def test_stage_is_abstract():
    assert {"validate_teams", "matches_count"} <= set(getattr(Stage, "__abstractmethods__", set()))
    with pytest.raises(TypeError):
        Stage("Этап", ["А", "Б"])


@pytest.mark.parametrize("n, rounds, expected", [(2, 1, 1), (4, 1, 6), (6, 2, 30), (10, 1, 45)])
def test_championship_matches(n, rounds, expected):
    teams = [f"Команда {i}" for i in range(n)]
    assert Championship("Чемпионат", teams, rounds=rounds).matches_count() == expected


def test_championship_validation():
    with pytest.raises(ValueError):
        Championship("Чемпионат", ["А"])
    with pytest.raises(ValueError):
        Championship("Чемпионат", ["А", "Б"], rounds=0)


@pytest.mark.parametrize("cls, ok, bad, matches", [
    (PlayoffCup, 4, [3, 5], 4),
    (RoundRobinCup, 3, [2, 4], 3),
])
def test_cups(cls, ok, bad, matches):
    stage = cls("Кубок", [f"К{i}" for i in range(ok)])
    assert stage.matches_count() == matches
    for n in bad:
        with pytest.raises(ValueError):
            cls("Кубок", [f"К{i}" for i in range(n)])


def test_stage_common_validation():
    with pytest.raises(ValueError):
        PlayoffCup("", ["А", "Б", "В", "Г"])
    with pytest.raises(ValueError):
        PlayoffCup("Кубок", ["А", "Б", "В", "а"])   # дубль без учёта регистра


def test_stage_inheritance():
    for cls in (Championship, PlayoffCup, RoundRobinCup):
        assert issubclass(cls, Stage)
        assert not getattr(cls, "__abstractmethods__", None), f"{cls.__name__} реализует не все абстрактные методы"
    assert "__str__" in vars(Stage), "__str__ должен быть один — в базовом классе"


def test_stage_str():
    assert str(PlayoffCup("Золотой кубок", ["А", "Б", "В", "Г"])) == "Золотой кубок: 4 команд(ы), 4 матч(ей)"
    assert str(Championship("Чемпионат", ["А", "Б", "В"], rounds=2)) == "Чемпионат: 3 команд(ы), 6 матч(ей)"


# ═══ 5. User ══════════════════════════════════════════════════════════
@pytest.fixture(autouse=True)
def clean_users():
    # очищаем занятые логины до и после каждого теста; пока reset() не написан — пропускаем
    if hasattr(User, "reset"):
        User.reset()
    yield
    if hasattr(User, "reset"):
        User.reset()


def test_user_login_normalized():
    assert User("  Sergey ", "owner").login == "sergey"


@pytest.mark.parametrize("login, role", [("", "admin"), ("   ", "admin"), ("ivan", "superuser")])
def test_user_validation(login, role):
    with pytest.raises(ValueError):
        User(login, role)


def test_user_unique_login():
    User("admin", "admin")
    with pytest.raises(ValueError):
        User("ADMIN", "photographer")


def test_user_failed_creation_does_not_take_login():
    with pytest.raises(ValueError):
        User("ivan", "unknown_role")
    User("ivan", "admin")   # логин не должен был «заняться»


def test_user_reset():
    User("anna", "admin")
    User.reset()
    User("anna", "admin")


@pytest.mark.parametrize("role, action, allowed", [
    ("owner", "manage_users", True),
    ("admin", "manage_users", False),
    ("admin", "edit_score", True),
    ("photographer", "upload_photos", True),
    ("photographer", "edit_score", False),
    ("admin", "fly_to_the_moon", False),
])
def test_user_can(role, action, allowed):
    assert User(f"user_{role}", role).can(action) is allowed


def test_user_permissions_is_class_attribute():
    assert "PERMISSIONS" in vars(User)


@pytest.mark.parametrize("password, ok", [
    ("Winnergy2027", True),
    ("Short1A", False),        # 7 символов
    ("winnergy2027", False),   # нет заглавной
    ("WINNERGY2027", False),   # нет строчной
    ("WinnergyCup", False),    # нет цифры
])
def test_user_password(password, ok):
    assert User.is_valid_password(password) is ok


def test_user_repr():
    assert repr(User("sergey", "owner")) == "User('sergey', role='owner')"
