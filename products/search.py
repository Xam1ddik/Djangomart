"""
Утилиты для поиска.

SQLite оператор LIKE (а значит и Django ``icontains``) регистронезависим
только для ASCII-символов — для кириллицы это не работает:

    'Хлеб белый' LIKE '%хлеб%'  -> False
    'Хлеб белый' LIKE '%Хлеб%'  -> True

Поэтому обычный ``Product.objects.filter(name__icontains=q)`` не находит
товары, если пользователь ввёл запрос в другом регистре, чем хранится
в базе — а это происходит почти всегда.

Чтобы поиск работал предсказуемо и одновременно поддерживал поиск по
slug (например ввод "bread" должен находить товар со slug
"white-bread"), здесь реализовано:

1. ``normalize`` — приведение произвольного текста к нижнему регистру
   через Python ``str.lower()``, который (в отличие от SQLite) корректно
   работает с кириллицей.
2. ``transliterate`` / ``build_search_slug`` — перевод кириллицы в
   латиницу и приведение к виду slug (``slugify``), чтобы можно было
   сопоставлять запрос напрямую с полем ``slug``.
"""
from django.utils.text import slugify

_CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def normalize(text: str) -> str:
    """Нижний регистр с корректной поддержкой кириллицы."""
    return (text or '').lower()


def transliterate(text: str) -> str:
    """Кириллица -> латиница, посимвольно (для сопоставления со slug)."""
    return ''.join(_CYRILLIC_TO_LATIN.get(ch, ch) for ch in normalize(text))


def build_search_slug(text: str) -> str:
    """Строит slug-подобный ключ из произвольного текста (в т.ч. кириллицы)."""
    return slugify(transliterate(text))


def matches(query: str, query_slug: str, *texts: str, slug: str = '') -> bool:
    """
    Проверяет, подходит ли объект под поисковый запрос.

    Сравнение идёт по двум направлениям:
    - обычный текст (name, description, ...) через регистронезависимое
      Python-сравнение;
    - slug объекта — против транслитерированного/slug-ифицированного
      запроса, что позволяет находить товары по латинскому slug.
    """
    haystack = normalize(' '.join(t for t in texts if t))
    if query and query in haystack:
        return True
    if query_slug and slug and query_slug in slug.lower():
        return True
    return False
