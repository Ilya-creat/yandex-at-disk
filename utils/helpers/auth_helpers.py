import os


def get_token_from_env(env_var: str = "YANDEX_DISK_TOKEN") -> str | None:
    return os.getenv(env_var)


def build_auth_header(token: str) -> dict:
    return {"Authorization": f"OAuth {token}"}
