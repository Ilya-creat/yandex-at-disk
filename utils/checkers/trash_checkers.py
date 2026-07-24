import allure

from models import ApiResponse


@allure.step("Проверить наличие {name} в списке корзины")
def assert_name_in_trash(response: ApiResponse, name: str) -> None:
    items = response.body.items
    assert any(item["name"] == name for item in items), f"{name} не найден в items корзины: {items}"
