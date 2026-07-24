from dataclasses import dataclass

from models.base import BaseModel


@dataclass
class ResourceModel(BaseModel):
    name: str
    path: str
    type: str
    created: str
    modified: str
    size: int = 0
    md5: str | None = None
    media_type: str | None = None
    custom_properties: dict | None = None
