from dataclasses import dataclass

from models.base import BaseModel


@dataclass
class LinkModel(BaseModel):
    href: str
    method: str
    templated: bool = False
