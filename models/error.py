from dataclasses import dataclass

from models.base import BaseModel


@dataclass
class ErrorModel(BaseModel):
    error: str
    message: str
    description: str | None = None
