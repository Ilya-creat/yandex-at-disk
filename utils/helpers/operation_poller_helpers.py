import time

from models import ApiResponse
from utils.helpers.api_client_helpers import ApiClient
from utils.routes.operations_routes import get_operation


def wait_for_operation(client: ApiClient, operation_id: str, timeout: int = 30, interval: float = 1.0) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        response = get_operation(client, operation_id)
        status = response.body.status
        if status != "in-progress":
            return status
        time.sleep(interval)
    raise TimeoutError(f"Operation {operation_id} did not finish within {timeout}s")


def resolve_maybe_async(client: ApiClient, response: ApiResponse, timeout: int = 30) -> None:
    if response.status_code != 202:
        return
    operation_id = response.raw.json()["href"].rstrip("/").rsplit("/", 1)[-1]
    status = wait_for_operation(client, operation_id, timeout=timeout)
    if status != "success":
        raise AssertionError(f"Operation {operation_id} finished with status={status}")
