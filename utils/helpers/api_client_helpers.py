import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.helpers.auth_helpers import build_auth_header

logger = logging.getLogger(__name__)


def _format_body(kwargs: dict) -> str:
    parts = []
    if kwargs.get("params"):
        parts.append(f"params={kwargs['params']}")
    if kwargs.get("json") is not None:
        parts.append(f"json={kwargs['json']}")
    if kwargs.get("data") is not None:
        data = kwargs["data"]
        size = len(data) if hasattr(data, "__len__") else "?"
        parts.append(f"data=<{size} bytes>")
    return " ".join(parts)


class ApiClient:
    def __init__(self, token: str, base_url: str = "https://cloud-api.yandex.net", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(build_auth_header(token))

        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=None,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._request("PATCH", path, **kwargs)

    def raw(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        logger.info("%s %s %s -> %s", method, url, _format_body(kwargs), response.status_code)
        return response

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, **kwargs)
        logger.info("%s %s %s -> %s", method, url, _format_body(kwargs), response.status_code)
        return response
