from dataclasses import dataclass, fields


@dataclass
class BaseRequest:
    def to_params(self) -> dict:
        params = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            key = f.metadata.get("alias", f.name)
            if isinstance(value, bool):
                value = "true" if value else "false"
            params[key] = value
        return params
