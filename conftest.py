import allure
import pytest
from dotenv import load_dotenv

from test_data.default_paths_data import DefaultPaths
from models.requests.resources import CreateResourceRequest, DeleteResourceRequest
from utils.helpers.api_client_helpers import ApiClient
from utils.helpers.auth_helpers import get_token_from_env
from utils.helpers.name_generator_helpers import random_folder_name
from utils.helpers.operation_poller_helpers import resolve_maybe_async
from utils.routes.resources_routes import create_resource, delete_resource

load_dotenv()


@pytest.fixture(scope="session")
def token() -> str:
    value = get_token_from_env()
    if not value:
        pytest.exit(
            "YANDEX_DISK_TOKEN не задан. Укажите его в файле .env (см. .env.example) "
            "или экспортируйте переменную окружения. Получить токен: https://oauth.yandex.ru"
        )
    return value


@pytest.fixture(scope="session")
def api_client(token: str) -> ApiClient:
    return ApiClient(token=token)


@pytest.fixture(scope="session")
def sandbox_root(api_client: ApiClient):
    path = f"{DefaultPaths.SANDBOX_ROOT}-{random_folder_name()}"
    with allure.step(f"[setup] Создать корневую папку песочницы {path}"):
        create_resource(api_client, CreateResourceRequest(path=path))

    yield path

    with allure.step(f"[teardown] Удалить корневую папку песочницы {path}"):
        response = delete_resource(
            api_client,
            DeleteResourceRequest(path=path, permanently=True, force_async=True),
        )
        resolve_maybe_async(api_client, response)


@pytest.fixture
def sandbox_folder(api_client: ApiClient, sandbox_root: str):
    path = f"{sandbox_root}/{random_folder_name()}"
    with allure.step(f"[setup] Создать папку песочницы {path}"):
        create_resource(api_client, CreateResourceRequest(path=path))

    yield path

    with allure.step(f"[teardown] Удалить папку песочницы {path}"):
        response = delete_resource(
            api_client, DeleteResourceRequest(path=path, permanently=True, force_async=True)
        )
        resolve_maybe_async(api_client, response)
