import allure

from models import ApiResponse


@allure.step("Проверить, что тело ответа соответствует ожидаемой модели")
def assert_body_is_instance(response: ApiResponse, model_cls: type) -> None:
    assert isinstance(response.body, model_cls), (
        f"Ожидалась модель {model_cls.__name__}, получено {type(response.body).__name__}: {response.body}"
    )
