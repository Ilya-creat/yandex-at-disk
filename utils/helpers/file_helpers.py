import hashlib
import os


def md5_of_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def build_test_file(size_bytes: int = 1024) -> bytes:
    return os.urandom(size_bytes)
