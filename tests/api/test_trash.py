import allure
import pytest

from models.requests.resources import CreateResourceRequest, DeleteResourceRequest
from models.requests.trash import TrashListRequest, TrashRestoreRequest
from utils.checkers.resource_checkers import assert_resource_exists
from utils.checkers.response_code_checkers import assert_response_code, assert_response_code_in
from utils.checkers.trash_checkers import assert_name_in_trash
from utils.helpers.name_generator_helpers import random_folder_name
from utils.helpers.operation_poller_helpers import resolve_maybe_async
from utils.helpers.trash_helpers import find_trash_path
from utils.routes.resources_routes import create_resource, delete_resource
from utils.routes.trash_routes import get_trash, restore_from_trash

pytestmark = pytest.mark.regress


@allure.story("API-AUTOTEST")
@allure.feature("Корзина")
class TestTrashPositive:
    @allure.title("Удалённый ресурс без permanently оказывается в корзине")
    @pytest.mark.destructive
    def test_delete_without_permanently_moves_resource_to_trash(self, api_client, sandbox_root):
        with allure.step("Создать папку"):
            path = f"{sandbox_root}/{random_folder_name()}"
            create_resource(api_client, CreateResourceRequest(path=path))

        with allure.step("Удалить папку без permanently"):
            response = delete_resource(api_client, DeleteResourceRequest(path=path, force_async=True))
            assert_response_code_in(response, (202, 204))
            resolve_maybe_async(api_client, response)

        with allure.step("Проверить, что папка появилась в корзине"):
            trash_response = get_trash(api_client, TrashListRequest())
            assert_response_code(trash_response, 200)
            assert_name_in_trash(trash_response, path.rsplit("/", 1)[-1])

    @allure.title("Ресурс из корзины можно восстановить на исходное место")
    @pytest.mark.destructive
    def test_restore_from_trash_recreates_resource(self, api_client, sandbox_root):
        with allure.step("Создать и удалить папку без permanently"):
            path = f"{sandbox_root}/{random_folder_name()}"
            create_resource(api_client, CreateResourceRequest(path=path))
            delete_response = delete_resource(api_client, DeleteResourceRequest(path=path, force_async=True))
            resolve_maybe_async(api_client, delete_response)

        with allure.step("Восстановить папку из корзины"):
            trash_path = find_trash_path(api_client, path)
            restore_response = restore_from_trash(api_client, TrashRestoreRequest(path=trash_path))
            assert_response_code_in(restore_response, (201, 202))
            resolve_maybe_async(api_client, restore_response)

        with allure.step("Проверить, что папка снова доступна на исходном пути"):
            assert_resource_exists(api_client, path)

        with allure.step("Убрать за собой: удалить папку без возможности восстановления"):
            cleanup_response = delete_resource(
                api_client, DeleteResourceRequest(path=path, permanently=True, force_async=True)
            )
            resolve_maybe_async(api_client, cleanup_response)
