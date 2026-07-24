from models import ApiResponse, LinkModel, ResourceListModel
from models.requests.base import BaseRequest
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.response_builder import allure_step, build_response

RESOURCES_PUBLISH = "/v1/disk/resources/publish"
RESOURCES_UNPUBLISH = "/v1/disk/resources/unpublish"
PUBLIC_RESOURCES = "/v1/disk/public/resources"


def publish_resource(client: ApiClient, request: BaseRequest) -> ApiResponse:
    with allure_step("PUT", RESOURCES_PUBLISH, "опубликовать ресурс"):
        response = client.put(RESOURCES_PUBLISH, params=request.to_params())
    return build_response(response, LinkModel)


def unpublish_resource(client: ApiClient, request: BaseRequest) -> ApiResponse:
    with allure_step("PUT", RESOURCES_UNPUBLISH, "закрыть доступ к ресурсу"):
        response = client.put(RESOURCES_UNPUBLISH, params=request.to_params())
    return build_response(response, LinkModel)


def get_public_resources(client: ApiClient) -> ApiResponse:
    with allure_step("GET", PUBLIC_RESOURCES, "получить список опубликованных ресурсов"):
        response = client.get(PUBLIC_RESOURCES)
    return build_response(response, ResourceListModel)
