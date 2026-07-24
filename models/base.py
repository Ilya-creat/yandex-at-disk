from dataclasses import dataclass, fields
from typing import TypeVar

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    @classmethod
    def from_dict(cls: type[T], data: dict) -> T:
        known = {f.name for f in fields(cls)}
        try:
            return cls(**{key: value for key, value in data.items() if key in known})
        except TypeError as exc:
            raise AssertionError(f"{cls.__name__} does not match response body: {exc}. Body: {data}") from exc
