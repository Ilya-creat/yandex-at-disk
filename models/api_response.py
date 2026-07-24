from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiResponse:
    status_code: int
    body: Any
    raw: requests.Response
