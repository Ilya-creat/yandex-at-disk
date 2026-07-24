from dataclasses import dataclass, field

from models.requests.base import BaseRequest


@dataclass
class ResourcePathRequest(BaseRequest):
    path: str | None = None


@dataclass
class CreateResourceRequest(ResourcePathRequest):
    pass


@dataclass
class GetResourceRequest(ResourcePathRequest):
    pass


@dataclass
class DeleteResourceRequest(ResourcePathRequest):
    permanently: bool | None = None
    force_async: bool | None = None


@dataclass
class PatchResourceRequest(ResourcePathRequest):
    pass


@dataclass
class MoveResourceRequest(BaseRequest):
    path: str
    from_path: str = field(metadata={"alias": "from"})
    overwrite: bool | None = None


@dataclass
class CopyResourceRequest(BaseRequest):
    path: str
    from_path: str = field(metadata={"alias": "from"})
    overwrite: bool | None = None


@dataclass
class UploadLinkRequest(ResourcePathRequest):
    overwrite: bool | None = None
    force_async: bool | None = None


@dataclass
class DownloadLinkRequest(ResourcePathRequest):
    pass


@dataclass
class FilesListRequest(BaseRequest):
    limit: int | None = None
    media_type: str | None = None


@dataclass
class CustomPropertiesBody:
    custom_properties: dict

    def to_json(self) -> dict:
        return {"custom_properties": self.custom_properties}
