import allure

from models import ApiResponse, ErrorModel


@allure.step("Проверить, что код ошибки равен {expected_error}")
def assert_error_response(response: ApiResponse, expected_error: str) -> None:
    assert isinstance(response.body, ErrorModel), (
        f"Ожидалось тело ErrorModel, получено {type(response.body)}: {response.raw.text}"
    )
    assert response.body.error == expected_error, (
        f"Ожидался error={expected_error!r}, получен error={response.body.error!r}"
    )
