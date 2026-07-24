import allure
import pytest

from models.requests.resources import CopyResourceRequest, CreateResourceRequest, MoveResourceRequest
from test_data.error_codes_data import ErrorCodes
from utils.checkers.error_checkers import assert_error_response
from utils.checkers.resource_checkers import assert_resource_exists
from utils.checkers.response_code_checkers import assert_response_code
from utils.helpers.name_generator_helpers import random_folder_name
from utils.routes.resources_routes import copy_resource, create_resource, move_resource

pytestmark = pytest.mark.regress


@allure.feature("API-AUTOTEST")
@allure.story("Файлы и папки")
class TestMoveCopyPositive:
    @allure.title("Пользователь может переместить папку")
    def test_move_folder_to_new_path_succeeds(self, api_client, sandbox_folder, sandbox_root):
        with allure.step("Переместить папку в новый путь"):
            destination = f"{sandbox_root}/{random_folder_name()}"
            response = move_resource(api_client, MoveResourceRequest(path=destination, from_path=sandbox_folder))

        with allure.step("Проверить код ответа и что папка появилась по новому пути"):
            assert_response_code(response, 201)
            assert_resource_exists(api_client, destination)

    @allure.title("Пользователь может скопировать папку, сохранив оригинал")
    def test_copy_folder_keeps_both_paths(self, api_client, sandbox_folder, sandbox_root):
        with allure.step("Скопировать папку"):
            destination = f"{sandbox_root}/{random_folder_name()}"
            response = copy_resource(api_client, CopyResourceRequest(path=destination, from_path=sandbox_folder))

        with allure.step("Проверить код ответа и что оба пути существуют"):
            assert_response_code(response, 201)
            assert_resource_exists(api_client, sandbox_folder)
            assert_resource_exists(api_client, destination)


@allure.feature("API-AUTOTEST")
@allure.story("Файлы и папки")
class TestMoveCopyNegative:
    @allure.title("Нельзя переместить папку поверх занятого пути без overwrite")
    def test_move_to_existing_path_without_overwrite_fails(self, api_client, sandbox_folder, sandbox_root):
        with allure.step("Подготовить занятый путь назначения"):
            other_folder = f"{sandbox_root}/{random_folder_name()}"
            create_resource(api_client, CreateResourceRequest(path=other_folder))

        with allure.step("Переместить папку в занятый путь без overwrite"):
            response = move_resource(api_client, MoveResourceRequest(path=other_folder, from_path=sandbox_folder))

        with allure.step("Проверить код и код ошибки"):
            assert_response_code(response, 409)
            assert_error_response(response, ErrorCodes.DISK_RESOURCE_ALREADY_EXISTS)
