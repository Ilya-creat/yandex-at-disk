import allure

from models import ApiResponse


@allure.step("Проверить наличие {path} в списке ответа")
def assert_path_in_listing(response: ApiResponse, path: str) -> None:
    items = response.body.items
    assert any(item["path"] == path for item in items), f"{path} не найден в items: {items}"
