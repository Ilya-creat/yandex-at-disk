import allure

from models import ApiResponse


@allure.step("Проверить, что код ответа равен {expected}")
def assert_response_code(response: ApiResponse, expected: int) -> None:
    assert response.status_code == expected, (
        f"Ожидался код {expected}, получен {response.status_code}. Тело: {response.body}"
    )


@allure.step("Проверить, что код ответа один из {expected}")
def assert_response_code_in(response: ApiResponse, expected: tuple) -> None:
    assert response.status_code in expected, (
        f"Ожидался один из {expected}, получен {response.status_code}. Тело: {response.body}"
    )
