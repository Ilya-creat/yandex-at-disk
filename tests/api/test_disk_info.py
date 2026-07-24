import allure
import pytest

from models import DiskInfoModel
from utils.checkers.disk_info_checkers import assert_used_space_non_negative
from utils.checkers.model_checkers import assert_body_is_instance
from utils.checkers.response_code_checkers import assert_response_code
from utils.routes.disk_info_routes import get_disk_info

pytestmark = pytest.mark.regress


@allure.story("Метаинформация о Диске")
@allure.feature("API-AUTOTEST")
class TestDiskInfoPositive:
    @allure.title("Метаинформация о Диске отдаётся в корректном формате")
    def test_get_disk_info_returns_valid_model(self, api_client):
        with allure.step("Запросить метаинформацию о Диске"):
            response = get_disk_info(api_client)

        with allure.step("Проверить код ответа и модель тела ответа"):
            assert_response_code(response, 200)
            assert_body_is_instance(response, DiskInfoModel)

    @allure.title("Занятое место на Диске не может быть отрицательным")
    def test_get_disk_info_used_space_is_not_negative(self, api_client):
        with allure.step("Запросить метаинформацию о Диске"):
            response = get_disk_info(api_client)

        with allure.step("Проверить used_space"):
            assert_used_space_non_negative(response)
