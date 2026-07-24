from dataclasses import dataclass

from models.requests.base import BaseRequest


@dataclass
class TrashListRequest(BaseRequest):
    path: str | None = None


@dataclass
class TrashDeleteRequest(BaseRequest):
    path: str | None = None
    force_async: bool | None = None


@dataclass
class TrashRestoreRequest(BaseRequest):
    path: str
    name: str | None = None
