from models import ApiResponse, DiskInfoModel
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.response_builder import allure_step, build_response

DISK = "/v1/disk"


def get_disk_info(client: ApiClient) -> ApiResponse:
    with allure_step("GET", DISK, "получить метаинформацию о Диске"):
        response = client.get(DISK)
    return build_response(response, DiskInfoModel)
