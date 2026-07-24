import uuid

from test_data.limits_data import Limits


def random_folder_name(prefix: str = "folder") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def random_file_name(prefix: str = "file", ext: str = "txt") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}.{ext}"


def oversized_name(ext: str = "txt") -> str:
    suffix = f".{ext}"
    base = "a" * (Limits.NAME_MAX_LEN - len(suffix) + 1)
    return f"{base}{suffix}"
