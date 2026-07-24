from models import ApiResponse, OperationModel
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.response_builder import allure_step, build_response

OPERATIONS = "/v1/disk/operations"


def operation_path(operation_id: str) -> str:
    return f"{OPERATIONS}/{operation_id}"


def get_operation(client: ApiClient, operation_id: str) -> ApiResponse:
    path = operation_path(operation_id)
    with allure_step("GET", path, "получить статус операции"):
        response = client.get(path)
    return build_response(response, OperationModel)
