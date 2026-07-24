from contextlib import contextmanager

import allure
import requests

from models import ApiResponse, ErrorModel


@contextmanager
def allure_step(method: str, path: str, description: str):
    with allure.step(f"{method} {path} — {description}"):
        yield


def build_response(response: requests.Response, model_cls) -> ApiResponse:
    body = None
    try:
        response.raise_for_status()
        if model_cls is not None:
            body = model_cls.from_dict(response.json())
    except requests.HTTPError:
        try:
            body = ErrorModel.from_dict(response.json())
        except ValueError:
            body = None
    except ValueError:
        body = None
    return ApiResponse(status_code=response.status_code, body=body, raw=response)
