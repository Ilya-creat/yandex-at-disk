import allure
import pytest

from models.requests.resources import FilesListRequest, UploadLinkRequest
from utils.checkers.listing_checkers import assert_path_in_listing
from utils.checkers.response_code_checkers import assert_response_code
from utils.helpers.file_helpers import build_test_file
from utils.helpers.name_generator_helpers import random_file_name
from utils.routes.resources_routes import get_files_list, get_last_uploaded, get_upload_link, upload_content

pytestmark = pytest.mark.regress


def _upload_file(api_client, path: str) -> None:
    link_response = get_upload_link(api_client, UploadLinkRequest(path=path, overwrite=True))
    upload_content(api_client, link_response.body, build_test_file())

@allure.story("Файлы и папки")
@allure.feature("API-AUTOTEST")
class TestFilesListingPositive:
    @allure.title("Загруженный файл попадает в плоский список файлов")
    @pytest.mark.destructive
    def test_files_listing_returns_uploaded_file(self, api_client, sandbox_folder):
        with allure.step("Загрузить файл"):
            path = f"{sandbox_folder}/{random_file_name()}"
            _upload_file(api_client, path)

        with allure.step("Запросить плоский список файлов"):
            response = get_files_list(api_client, FilesListRequest(limit=200))

        with allure.step("Проверить код ответа и наличие файла в списке"):
            assert_response_code(response, 200)
            assert_path_in_listing(response, path)

    @allure.title("Загруженный файл попадает в список последних загруженных")
    @pytest.mark.destructive
    def test_last_uploaded_returns_uploaded_file(self, api_client, sandbox_folder):
        with allure.step("Загрузить файл"):
            path = f"{sandbox_folder}/{random_file_name()}"
            _upload_file(api_client, path)

        with allure.step("Запросить список последних загруженных файлов"):
            response = get_last_uploaded(api_client, FilesListRequest(limit=200))

        with allure.step("Проверить код ответа и наличие файла в списке"):
            assert_response_code(response, 200)
            assert_path_in_listing(response, path)
