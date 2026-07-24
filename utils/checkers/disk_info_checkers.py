import allure

from models import ApiResponse


@allure.step("Проверить, что used_space не отрицательное")
def assert_used_space_non_negative(response: ApiResponse) -> None:
    used_space = response.body.used_space
    assert used_space >= 0, f"Ожидалось used_space >= 0, получено {used_space}"
