from dataclasses import dataclass, field

from models.base import BaseModel


@dataclass
class ResourceListModel(BaseModel):
    items: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ResourceListModel":
        if "items" not in data and "_embedded" in data:
            data = data["_embedded"]
        return super().from_dict(data)
