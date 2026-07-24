import allure

from utils.helpers.file_helpers import md5_of_bytes


@allure.step("Проверить совпадение md5 скачанного содержимого с исходным")
def assert_content_md5_matches(actual: bytes, expected: bytes) -> None:
    actual_md5, expected_md5 = md5_of_bytes(actual), md5_of_bytes(expected)
    assert actual_md5 == expected_md5, f"Ожидался md5={expected_md5}, получен md5={actual_md5}"
