from dataclasses import dataclass

from models.base import BaseModel


@dataclass
class OperationModel(BaseModel):
    status: str
