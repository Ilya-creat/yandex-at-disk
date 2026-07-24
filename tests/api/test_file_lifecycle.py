import allure
import pytest

from models import DiskInfoModel
from models.requests.resources import (
    CopyResourceRequest,
    DeleteResourceRequest,
    DownloadLinkRequest,
    GetResourceRequest,
    MoveResourceRequest,
    UploadLinkRequest,
)
from models.requests.trash import TrashRestoreRequest
from utils.checkers.content_checkers import assert_content_md5_matches
from utils.checkers.model_checkers import assert_body_is_instance
from utils.checkers.resource_checkers import assert_resource_exists
from utils.checkers.response_code_checkers import assert_response_code, assert_response_code_in
from utils.helpers.file_helpers import build_test_file
from utils.helpers.name_generator_helpers import random_file_name, random_folder_name
from utils.helpers.operation_poller_helpers import resolve_maybe_async
from utils.helpers.trash_helpers import find_trash_path
from utils.routes.disk_info_routes import get_disk_info
from utils.routes.resources_routes import (
    copy_resource,
    delete_resource,
    download_content,
    get_download_link,
    get_resource,
    get_upload_link,
    move_resource,
    upload_content,
)
from utils.routes.trash_routes import restore_from_trash

pytestmark = pytest.mark.regress


@allure.story("API-AUTOTEST")
@allure.feature("Интеграционные сценарии")
class TestFileLifecyclePositive:
    @allure.title("Загрузка файла увеличивает занятое место на Диске, удаление — освобождает")
    @pytest.mark.destructive
    def test_upload_and_delete_updates_disk_usage(self, api_client, sandbox_folder):
        with allure.step("Запросить состояние Диска до загрузки"):
            info_before = get_disk_info(api_client)
            assert_body_is_instance(info_before, DiskInfoModel)

        with allure.step("Загрузить файл"):
            path = f"{sandbox_folder}/{random_file_name()}"
            content = build_test_file(size_bytes=65536)

            upload_link = get_upload_link(api_client, UploadLinkRequest(path=path, overwrite=True))
            put_response = upload_content(api_client, upload_link.body, content)
            assert_response_code(put_response, 201)

        with allure.step("Убедиться, что занятое место на Диске увеличилось"):
            info_after_upload = get_disk_info(api_client)
            assert info_after_upload.body.used_space > info_before.body.used_space

        with allure.step("Скачать файл и сверить содержимое"):
            download_link = get_download_link(api_client, DownloadLinkRequest(path=path))
            downloaded = download_content(api_client, download_link.body)
            assert_response_code(downloaded, 200)
            assert_content_md5_matches(downloaded.raw.content, content)

        with allure.step("Удалить файл без возможности восстановления"):
            delete_response = delete_resource(api_client, DeleteResourceRequest(path=path, permanently=True))
            assert_response_code(delete_response, 204)

        with allure.step("Убедиться, что файл больше не существует"):
            meta_after_delete = get_resource(api_client, GetResourceRequest(path=path))
            assert_response_code(meta_after_delete, 404)

        with allure.step("Убедиться, что занятое место на Диске уменьшилось обратно"):
            info_after_delete = get_disk_info(api_client)
            assert info_after_delete.body.used_space <= info_after_upload.body.used_space

    @allure.title("Файл переживает копирование, перемещение папки и удаление в корзину с восстановлением")
    @pytest.mark.destructive
    def test_copy_move_and_restore_folder_with_file(self, api_client, sandbox_folder, sandbox_root):
        with allure.step("Загрузить файл в исходную папку"):
            file_name = random_file_name()
            upload_link = get_upload_link(
                api_client, UploadLinkRequest(path=f"{sandbox_folder}/{file_name}", overwrite=True)
            )
            upload_content(api_client, upload_link.body, build_test_file())

        with allure.step("Скопировать папку с файлом"):
            copy_destination = f"{sandbox_root}/{random_folder_name()}"
            copy_response = copy_resource(
                api_client, CopyResourceRequest(path=copy_destination, from_path=sandbox_folder)
            )
            assert_response_code_in(copy_response, (201, 202))
            resolve_maybe_async(api_client, copy_response)
            assert_resource_exists(api_client, f"{copy_destination}/{file_name}")

        with allure.step("Переместить копию папки"):
            move_destination = f"{sandbox_root}/{random_folder_name()}"
            move_response = move_resource(
                api_client, MoveResourceRequest(path=move_destination, from_path=copy_destination)
            )
            assert_response_code_in(move_response, (201, 202))
            resolve_maybe_async(api_client, move_response)
            assert_resource_exists(api_client, f"{move_destination}/{file_name}")

        with allure.step("Удалить перемещённую папку в корзину и восстановить её обратно"):
            delete_response = delete_resource(api_client, DeleteResourceRequest(path=move_destination, force_async=True))
            resolve_maybe_async(api_client, delete_response)

            trash_path = find_trash_path(api_client, move_destination)
            restore_response = restore_from_trash(api_client, TrashRestoreRequest(path=trash_path))
            resolve_maybe_async(api_client, restore_response)

        with allure.step("Убедиться, что папка и файл в ней восстановлены"):
            assert_resource_exists(api_client, f"{move_destination}/{file_name}")

        with allure.step("Убрать за собой: удалить папку без возможности восстановления"):
            cleanup_response = delete_resource(
                api_client, DeleteResourceRequest(path=move_destination, permanently=True, force_async=True)
            )
            resolve_maybe_async(api_client, cleanup_response)
