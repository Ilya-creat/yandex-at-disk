from models import ApiResponse, LinkModel, ResourceListModel
from models.requests.trash import TrashDeleteRequest, TrashListRequest, TrashRestoreRequest
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.response_builder import allure_step, build_response

TRASH_RESOURCES = "/v1/disk/trash/resources"
TRASH_RESOURCES_RESTORE = "/v1/disk/trash/resources/restore"


def get_trash(client: ApiClient, request: TrashListRequest) -> ApiResponse:
    with allure_step("GET", TRASH_RESOURCES, "получить содержимое корзины"):
        response = client.get(TRASH_RESOURCES, params=request.to_params())
    return build_response(response, ResourceListModel)


def delete_trash(client: ApiClient, request: TrashDeleteRequest) -> ApiResponse:
    with allure_step("DELETE", TRASH_RESOURCES, "очистить корзину"):
        response = client.delete(TRASH_RESOURCES, params=request.to_params())
    return build_response(response, None)


def restore_from_trash(client: ApiClient, request: TrashRestoreRequest) -> ApiResponse:
    with allure_step("PUT", TRASH_RESOURCES_RESTORE, "восстановить ресурс из корзины"):
        response = client.put(TRASH_RESOURCES_RESTORE, params=request.to_params())
    return build_response(response, LinkModel)
