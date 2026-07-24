from dataclasses import dataclass

from models.base import BaseModel


@dataclass
class DiskInfoModel(BaseModel):
    total_space: int
    used_space: int
    trash_size: int
