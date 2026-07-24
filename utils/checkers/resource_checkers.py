import allure

from models import ApiResponse
from models.requests.resources import GetResourceRequest
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.resources_routes import get_resource


@allure.step("Проверить, что тип ресурса равен {expected_type}")
def assert_resource_type(response: ApiResponse, expected_type: str) -> None:
    actual_type = response.body.type
    assert actual_type == expected_type, f"Ожидался type={expected_type!r}, получен type={actual_type!r}"


@allure.step("Проверить, что ресурс {path} существует")
def assert_resource_exists(client: ApiClient, path: str) -> None:
    response = get_resource(client, GetResourceRequest(path=path))
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"


@allure.step("Проверить, что custom_properties[{key}] равно {expected_value}")
def assert_custom_property_value(response: ApiResponse, key: str, expected_value) -> None:
    custom_properties = response.body.custom_properties or {}
    actual_value = custom_properties.get(key)
    assert actual_value == expected_value, (
        f"Ожидалось custom_properties[{key!r}]={expected_value!r}, получено {actual_value!r}"
    )


@allure.step("Проверить, что custom_properties[{key}] отсутствует")
def assert_custom_property_absent(response: ApiResponse, key: str) -> None:
    custom_properties = response.body.custom_properties or {}
    assert key not in custom_properties, (
        f"Ожидалось отсутствие {key!r}, получено custom_properties={custom_properties!r}"
    )
