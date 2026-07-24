import allure
import pytest

from models.requests.resources import CreateResourceRequest, GetResourceRequest
from test_data.error_codes_data import ErrorCodes
from utils.checkers.error_checkers import assert_error_response
from utils.checkers.response_code_checkers import assert_response_code
from utils.helpers.api_client_helpers import ApiClient
from utils.helpers.name_generator_helpers import oversized_name, random_folder_name
from utils.routes.disk_info_routes import get_disk_info
from utils.routes.resources_routes import create_resource, get_resource

pytestmark = pytest.mark.regress


@allure.story("API-AUTOTEST")
@allure.feature("Негативные / общие")
class TestNegativeCommonNegative:
    @allure.title("Невалидный токен авторизации отклоняется")
    def test_request_with_invalid_token_is_rejected(self):
        with allure.step("Запросить метаинформацию о Диске с невалидным токеном"):
            client = ApiClient(token="invalid-token-0000000000")
            response = get_disk_info(client)

        with allure.step("Проверить код ответа"):
            assert_response_code(response, 401)

    @allure.title("Запрос без обязательного параметра отклоняется")
    def test_request_missing_required_path_param_is_rejected(self, api_client):
        with allure.step("Запросить метаинформацию о ресурсе без параметра path"):
            response = get_resource(api_client, GetResourceRequest())

        with allure.step("Проверить код ответа"):
            assert_response_code(response, 400)

    @allure.title("Имя ресурса сверх лимита длины не создаёт ресурс")
    def test_create_folder_with_name_over_limit_fails(self, api_client, sandbox_root):
        with allure.step("Создать папку с именем на один символ длиннее лимита"):
            path = f"{sandbox_root}/{oversized_name()}"
            response = create_resource(api_client, CreateResourceRequest(path=path))

        with allure.step("Проверить код и код ошибки"):
            assert_response_code(response, 404)
            assert_error_response(response, ErrorCodes.DISK_NOT_FOUND_ERROR)

    @allure.title("Слишком длинный путь ресурса не создаёт ресурс")
    def test_create_folder_with_oversized_path_fails(self, api_client, sandbox_root):
        with allure.step("Создать папку по пути, превышающему допустимую длину"):
            long_segment = random_folder_name() * 2000
            path = f"{sandbox_root}/{long_segment}"
            response = create_resource(api_client, CreateResourceRequest(path=path))

        with allure.step("Проверить код ответа"):
            assert_response_code(response, 414)
