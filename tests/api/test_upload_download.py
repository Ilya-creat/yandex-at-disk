import allure
import pytest

from models import LinkModel
from models.requests.resources import DownloadLinkRequest, GetResourceRequest, UploadLinkRequest
from utils.checkers.content_checkers import assert_content_md5_matches
from utils.checkers.model_checkers import assert_body_is_instance
from utils.checkers.response_code_checkers import assert_response_code, assert_response_code_in
from utils.helpers.file_helpers import build_test_file
from utils.helpers.name_generator_helpers import random_file_name
from utils.routes.resources_routes import (
    download_content,
    get_download_link,
    get_resource,
    get_upload_link,
    upload_content,
)

pytestmark = pytest.mark.regress


@allure.story("Файлы и папки")
@allure.feature("API-AUTOTEST")
class TestUploadDownloadPositive:
    @allure.title("Скачанный файл идентичен загруженному")
    @pytest.mark.destructive
    def test_upload_then_download_file_matches_md5(self, api_client, sandbox_folder):
        with allure.step("Подготовить путь и содержимое файла"):
            path = f"{sandbox_folder}/{random_file_name()}"
            content = build_test_file()

        with allure.step("Загрузить файл"):
            upload_link_response = get_upload_link(api_client, UploadLinkRequest(path=path, overwrite=True))
            assert_response_code(upload_link_response, 200)
            assert_body_is_instance(upload_link_response, LinkModel)

            put_response = upload_content(api_client, upload_link_response.body, content)
            assert_response_code(put_response, 201)

        with allure.step("Скачать файл обратно"):
            download_link_response = get_download_link(api_client, DownloadLinkRequest(path=path))
            assert_response_code(download_link_response, 200)
            assert_body_is_instance(download_link_response, LinkModel)

            get_response = download_content(api_client, download_link_response.body)
            assert_response_code(get_response, 200)

        with allure.step("Сравнить md5 исходного и скачанного содержимого"):
            assert_content_md5_matches(get_response.raw.content, content)

    @allure.title("Загрузка файла с force_async завершается успешно")
    @pytest.mark.destructive
    @pytest.mark.slow
    def test_upload_with_force_async_completes_successfully(self, api_client, sandbox_folder):
        with allure.step("Подготовить путь и содержимое файла"):
            path = f"{sandbox_folder}/{random_file_name()}"
            content = build_test_file()

        with allure.step("Загрузить файл с force_async"):
            upload_link_response = get_upload_link(
                api_client, UploadLinkRequest(path=path, overwrite=True, force_async=True)
            )
            assert_response_code(upload_link_response, 200)

            put_response = upload_content(api_client, upload_link_response.body, content)
            assert_response_code_in(put_response, (201, 202))

        with allure.step("Убедиться, что файл появился на Диске"):
            meta_response = get_resource(api_client, GetResourceRequest(path=path))
            assert_response_code(meta_response, 200)
