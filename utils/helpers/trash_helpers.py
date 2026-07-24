import allure

from models.requests.trash import TrashListRequest
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.trash_routes import get_trash


@allure.step("Найти путь в корзине для {origin_path}")
def find_trash_path(client: ApiClient, origin_path: str) -> str:
    response = get_trash(client, TrashListRequest(path="trash:/"))
    items = response.body.items
    for item in items:
        if item.get("origin_path") == origin_path:
            return item["path"]
    raise AssertionError(f"{origin_path} не найден в корзине. items: {items}")
