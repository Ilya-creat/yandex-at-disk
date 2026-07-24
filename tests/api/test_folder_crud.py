import allure
import pytest

from models import ResourceModel
from models.requests.resources import CreateResourceRequest, DeleteResourceRequest, GetResourceRequest
from test_data.error_codes_data import ErrorCodes
from utils.checkers.error_checkers import assert_error_response
from utils.checkers.model_checkers import assert_body_is_instance
from utils.checkers.resource_checkers import assert_resource_type
from utils.checkers.response_code_checkers import assert_response_code
from utils.helpers.name_generator_helpers import random_folder_name
from utils.routes.resources_routes import create_resource, delete_resource, get_resource

pytestmark = pytest.mark.regress

@allure.feature("API-AUTOTEST")
@allure.story("Файлы и папки")
class TestFolderCrudPositive:
    @allure.title("Пользователь может создать папку")
    def test_create_folder_succeeds(self, api_client, sandbox_root):
        with allure.step("Подготовить путь новой папки"):
            path = f"{sandbox_root}/{random_folder_name()}"

        with allure.step("Создать папку"):
            response = create_resource(api_client, CreateResourceRequest(path=path))

        with allure.step("Проверить код ответа"):
            assert_response_code(response, 201)

    @allure.title("Пользователь может получить метаданные папки")
    def test_get_folder_meta_returns_dir_type(self, api_client, sandbox_folder):
        with allure.step("Запросить метаданные папки"):
            response = get_resource(api_client, GetResourceRequest(path=sandbox_folder))

        with allure.step("Проверить код ответа, модель и тип ресурса"):
            assert_response_code(response, 200)
            assert_body_is_instance(response, ResourceModel)
            assert_resource_type(response, "dir")

    @allure.title("Пользователь может безвозвратно удалить папку")
    def test_delete_folder_succeeds(self, api_client, sandbox_root):
        with allure.step("Создать папку для удаления"):
            path = f"{sandbox_root}/{random_folder_name()}"
            create_resource(api_client, CreateResourceRequest(path=path))

        with allure.step("Удалить папку без возможности восстановления"):
            response = delete_resource(api_client, DeleteResourceRequest(path=path, permanently=True))

        with allure.step("Проверить код ответа"):
            assert_response_code(response, 204)

@allure.feature("API-AUTOTEST")
@allure.story("Файлы и папки")
class TestFolderCrudNegative:
    @allure.title("Запрос метаданных несуществующей папки завершается ошибкой")
    def test_get_meta_for_missing_folder_fails(self, api_client, sandbox_root):
        with allure.step("Запросить метаданные папки, которой не существует"):
            path = f"{sandbox_root}/{random_folder_name()}"
            response = get_resource(api_client, GetResourceRequest(path=path))

        with allure.step("Проверить код и код ошибки"):
            assert_response_code(response, 404)
            assert_error_response(response, ErrorCodes.DISK_NOT_FOUND_ERROR)

    @allure.title("Нельзя создать папку поверх уже существующей")
    def test_create_folder_that_already_exists_fails(self, api_client, sandbox_folder):
        with allure.step("Повторно создать уже существующую папку"):
            response = create_resource(api_client, CreateResourceRequest(path=sandbox_folder))

        with allure.step("Проверить код и код ошибки"):
            assert_response_code(response, 409)
            assert_error_response(response, ErrorCodes.DISK_PATH_POINTS_TO_EXISTENT_DIRECTORY_ERROR)
