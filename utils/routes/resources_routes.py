import requests

from models import ApiResponse, ErrorModel, LinkModel, ResourceListModel, ResourceModel
from models.requests.resources import (
    CopyResourceRequest,
    CustomPropertiesBody,
    DeleteResourceRequest,
    DownloadLinkRequest,
    FilesListRequest,
    GetResourceRequest,
    MoveResourceRequest,
    PatchResourceRequest,
    ResourcePathRequest,
    UploadLinkRequest,
)
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.response_builder import allure_step, build_response

RESOURCES = "/v1/disk/resources"
RESOURCES_UPLOAD = "/v1/disk/resources/upload"
RESOURCES_DOWNLOAD = "/v1/disk/resources/download"
RESOURCES_MOVE = "/v1/disk/resources/move"
RESOURCES_COPY = "/v1/disk/resources/copy"
RESOURCES_FILES = "/v1/disk/resources/files"
RESOURCES_LAST_UPLOADED = "/v1/disk/resources/last-uploaded"


def get_resource(client: ApiClient, request: GetResourceRequest) -> ApiResponse:
    with allure_step("GET", RESOURCES, "получить метаинформацию о ресурсе"):
        response = client.get(RESOURCES, params=request.to_params())
    return build_response(response, ResourceModel)


def create_resource(client: ApiClient, request: ResourcePathRequest) -> ApiResponse:
    with allure_step("PUT", RESOURCES, "создать папку"):
        response = client.put(RESOURCES, params=request.to_params())
    return build_response(response, LinkModel)


def delete_resource(client: ApiClient, request: DeleteResourceRequest) -> ApiResponse:
    with allure_step("DELETE", RESOURCES, "удалить ресурс"):
        response = client.delete(RESOURCES, params=request.to_params())
    return build_response(response, None)


def patch_resource(client: ApiClient, request: PatchResourceRequest, body: CustomPropertiesBody) -> ApiResponse:
    with allure_step("PATCH", RESOURCES, "изменить пользовательские свойства ресурса"):
        response = client.patch(RESOURCES, params=request.to_params(), json=body.to_json())
    return build_response(response, ResourceModel)


def move_resource(client: ApiClient, request: MoveResourceRequest) -> ApiResponse:
    with allure_step("POST", RESOURCES_MOVE, "переместить ресурс"):
        response = client.post(RESOURCES_MOVE, params=request.to_params())
    return build_response(response, LinkModel)


def copy_resource(client: ApiClient, request: CopyResourceRequest) -> ApiResponse:
    with allure_step("POST", RESOURCES_COPY, "скопировать ресурс"):
        response = client.post(RESOURCES_COPY, params=request.to_params())
    return build_response(response, LinkModel)


def get_upload_link(client: ApiClient, request: UploadLinkRequest) -> ApiResponse:
    with allure_step("GET", RESOURCES_UPLOAD, "получить ссылку для загрузки файла"):
        response = client.get(RESOURCES_UPLOAD, params=request.to_params())
    return build_response(response, LinkModel)


def get_download_link(client: ApiClient, request: DownloadLinkRequest) -> ApiResponse:
    with allure_step("GET", RESOURCES_DOWNLOAD, "получить ссылку для скачивания файла"):
        response = client.get(RESOURCES_DOWNLOAD, params=request.to_params())
    return build_response(response, LinkModel)


def upload_content(client: ApiClient, link: LinkModel, content: bytes) -> ApiResponse:
    with allure_step(link.method, link.href, "загрузить содержимое файла по ссылке"):
        response = client.raw(link.method, link.href, data=content)
    body = None
    try:
        response.raise_for_status()
    except requests.HTTPError:
        try:
            body = ErrorModel.from_dict(response.json())
        except ValueError:
            body = None
    return ApiResponse(status_code=response.status_code, body=body, raw=response)


def download_content(client: ApiClient, link: LinkModel) -> ApiResponse:
    with allure_step(link.method, link.href, "скачать содержимое файла по ссылке"):
        response = client.raw(link.method, link.href)
    body = None
    try:
        response.raise_for_status()
    except requests.HTTPError:
        try:
            body = ErrorModel.from_dict(response.json())
        except ValueError:
            body = None
    return ApiResponse(status_code=response.status_code, body=body, raw=response)


def get_files_list(client: ApiClient, request: FilesListRequest) -> ApiResponse:
    with allure_step("GET", RESOURCES_FILES, "получить плоский список файлов"):
        response = client.get(RESOURCES_FILES, params=request.to_params())
    return build_response(response, ResourceListModel)


def get_last_uploaded(client: ApiClient, request: FilesListRequest) -> ApiResponse:
    with allure_step("GET", RESOURCES_LAST_UPLOADED, "получить последние загруженные файлы"):
        response = client.get(RESOURCES_LAST_UPLOADED, params=request.to_params())
    return build_response(response, ResourceListModel)
