# yandex-at-disk

Автотесты для REST API Яндекс.Диска (`https://cloud-api.yandex.net`).

Тесты работают внутри выделенной песочницы `disk:/pytest-sandbox` — эта папка
создаётся перед прогоном и полностью удаляется после, включая корзину для тестов, которые её используют.
Остальной диск не затрагивается.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Настройка токена

1. Получите OAuth-токен на https://oauth.yandex.ru.
2. Скопируйте `.env.example` в `.env` и впишите токен:

```
YANDEX_DISK_TOKEN=<ваш токен>
```

## Запуск тестов

```bash
pytest                                    # все тесты
pytest -m regress                         # регрессионный набор (сейчас это все тесты)
pytest -m "not destructive"               # только немутирующие тесты
pytest --alluredir=allure-results         # с allure-отчётом
```

## Структура проекта

```
test_data/            — статичные данные: коды ошибок, media_type, лимиты, дефолтные пути (*_data.py)
  requests/            — dataclass-модели параметров/тела запроса, сгруппированные как в API (*_request.py)
models/                — dataclass-модели тел ответа (ResourceModel, DiskInfoModel, LinkModel, OperationModel,
                         ErrorModel, ResourceListModel) и ApiResponse — обёртка над сырым requests.Response
utils/
  routes/              — вызовы ручек, сгруппированные как в документации API (Файлы и папки, Корзина,
                         Метаинформация о Диске, Операции, Публичные файлы и папки). Каждая функция —
                         allure.step, парсит JSON в модель из models/ и возвращает ApiResponse
  helpers/             — ApiClient, авторизация, генерация имён, работа с файлами, поллинг операций (*_helpers.py)
  checkers/            — ассерты по коду ответа, ошибке, модели ответа и предметной области (*_checkers.py)
tests/api/             — тестовые файлы (*_test.py — нестандартное именование, задано в pytest.ini).
                         Тесты сгруппированы в классы <Файл>Positive / <Файл>Negative
```