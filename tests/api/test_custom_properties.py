import allure
import pytest

from test_data.limits_data import Limits
from models.requests.resources import CustomPropertiesBody, PatchResourceRequest
from utils.checkers.resource_checkers import assert_custom_property_absent, assert_custom_property_value
from utils.checkers.response_code_checkers import assert_response_code
from utils.routes.resources_routes import patch_resource

pytestmark = pytest.mark.regress


@allure.story("API-AUTOTEST")
@allure.feature("Файлы и папки")
class TestCustomPropertiesPositive:
    @allure.title("Пользователь может задать пользовательское свойство ресурса")
    @pytest.mark.destructive
    def test_patch_sets_custom_property(self, api_client, sandbox_folder):
        with allure.step("Установить пользовательское свойство"):
            response = patch_resource(
                api_client,
                PatchResourceRequest(path=sandbox_folder),
                CustomPropertiesBody(custom_properties={"tested_by": "pytest"}),
            )

        with allure.step("Проверить код ответа и значение свойства"):
            assert_response_code(response, 200)
            assert_custom_property_value(response, "tested_by", "pytest")

    @allure.title("Значение null в пользовательском свойстве удаляет ключ")
    @pytest.mark.destructive
    def test_patch_with_null_value_removes_key(self, api_client, sandbox_folder):
        with allure.step("Установить пользовательское свойство"):
            patch_resource(
                api_client,
                PatchResourceRequest(path=sandbox_folder),
                CustomPropertiesBody(custom_properties={"tested_by": "pytest"}),
            )

        with allure.step("Передать null тем же ключом"):
            response = patch_resource(
                api_client,
                PatchResourceRequest(path=sandbox_folder),
                CustomPropertiesBody(custom_properties={"tested_by": None}),
            )

        with allure.step("Проверить код ответа и отсутствие ключа"):
            assert_response_code(response, 200)
            assert_custom_property_absent(response, "tested_by")

    @allure.title("Пользовательские свойства принимаются на максимальной допустимой длине")
    @pytest.mark.destructive
    def test_patch_at_max_serialized_length_is_accepted(self, api_client, sandbox_folder):
        with allure.step("Установить свойство на границе Limits.CUSTOM_PROPERTIES_MAX_SERIALIZED_LEN"):
            padding_len = Limits.CUSTOM_PROPERTIES_MAX_SERIALIZED_LEN - len('{"value":""}')
            response = patch_resource(
                api_client,
                PatchResourceRequest(path=sandbox_folder),
                CustomPropertiesBody(custom_properties={"value": "a" * max(padding_len, 0)}),
            )

        with allure.step("Проверить код ответа"):
            assert_response_code(response, 200)
