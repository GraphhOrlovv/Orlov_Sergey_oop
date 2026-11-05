"""
Набор 01 — разминка: строки, списки, словари.

Как работать:
1. Напиши код вместо `pass` в каждой функции.
2. Запусти тесты:  pytest -v test_tasks_01.py
3. Когда всё зелёное (или застрял) — пришли этот файл в чат.

Правила: только стандартная библиотека Python, без импорта готовых решений
из интернета. Можно пользоваться документацией.
"""


# ─── Задача 1. Палиндром ──────────────────────────────────────────────
def is_palindrome(text: str) -> bool:
    """
    Вернуть True, если строка читается одинаково слева направо и справа налево.
    Регистр, пробелы и знаки препинания НЕ учитываются.

    is_palindrome("А роза упала на лапу Азора")  -> True
    is_palindrome("Madam, I'm Adam")             -> True
    is_palindrome("Python")                      -> False
    is_palindrome("")                            -> True
    """
    text_reverse = text[::-1].lower().replace(' ', '').replace(',', '').replace('!', '').replace("'", "")
    return text_reverse == text.lower().replace(' ', '').replace(',', '').replace('!', '').replace("'", "")


# ─── Задача 2. Частота слов ───────────────────────────────────────────
def word_count(text: str) -> dict[str, int]:
    """
    Посчитать, сколько раз встречается каждое слово.
    - регистр не важен (всё приводим к нижнему);
    - знаки препинания . , ! ? : ; убираем;
    - слова разделены пробелами (их может быть несколько подряд).

    word_count("Тест, тест! И ещё   тест.") -> {"тест": 3, "и": 1, "ещё": 1}
    word_count("")                         -> {}
    """
    word_dict = dict()
    for word in text.split():
        word = word.lower().strip('. , ! ? : ;')
        word_dict[word] = word_dict.get(word, 0) + 1
    return word_dict


# ─── Задача 3. Группировка ответов API ────────────────────────────────
def group_by_status(responses: list[dict]) -> dict[int, list[str]]:
    """
    На вход — список ответов вида {"url": "/users", "status": 200}.
    Вернуть словарь: статус -> список url с этим статусом (в исходном порядке).

    group_by_status([
        {"url": "/users", "status": 200},
        {"url": "/teams", "status": 500},
        {"url": "/games", "status": 200},
    ]) -> {200: ["/users", "/games"], 500: ["/teams"]}
    """
    statuses_dict = dict()
    for response in responses:
        status = response["status"]
        url = response["url"]
        if status in statuses_dict:
            statuses_dict[status].append(url)
        else:
            statuses_dict[status] = [url]
    return statuses_dict


# ─── Задача 4. Что сломалось? ─────────────────────────────────────────
def diff_ids(expected: list[int], actual: list[int]) -> dict[str, list[int]]:
    """
    Сравнить ожидаемые и пришедшие из API id.
    Вернуть {"missing": [...], "extra": [...]}:
      missing — есть в expected, но нет в actual;
      extra   — есть в actual, но нет в expected.
    Оба списка — без повторов и отсортированы по возрастанию.

    diff_ids([1, 2, 3, 4], [2, 4, 5, 5]) -> {"missing": [1, 3], "extra": [5]}
    """
    missing_id = sorted(list(set(expected) - set(actual)))
    extra_id = sorted(list(set(actual) - set(expected)))
    result = {"missing": missing_id, "extra": extra_id}
    return result


# ─── Задача 5. Плоский словарь ────────────────────────────────────────
def flatten(data: dict, parent: str = "") -> dict:
    """
    «Расплющить» вложенный словарь: ключи склеиваются через точку.
    Вложенность может быть любой глубины. Значения, которые не dict, — оставляем как есть.

    flatten({"user": {"name": "Ann", "address": {"city": "Москва"}}, "id": 1})
    -> {"user.name": "Ann", "user.address.city": "Москва", "id": 1}
    """
    new_dict = dict()
    for key, value in data.items():
        new_key = f"{parent}.{key}" if parent else key
        if isinstance(value, dict):
            new_dict.update(flatten(value, new_key))
        else:
            new_dict[new_key] = value
    return new_dict

