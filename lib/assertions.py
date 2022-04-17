from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст '{response.text}'"
        assert name in response_as_dict, f"Ответ JSON нет ключа  '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:

            assert False, f"Ответ не в формате JSON. Текст '{response.text}'"

        assert name in response_as_dict, f"В JSON нет ключа '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:

            assert False, f"Ответ не в формате JSON. Текст '{response.text}'"
        for name in names:
            assert name in response_as_dict, f"В JSON нет ключа '{name}'"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:

            assert False, f"Ответ не в формате JSON. Текст '{response.text}'"
        for name in names:
            assert name not in response_as_dict, f"В JSON есть ключ/чи '{name}'"

    @staticmethod
    def assert_status_code(response: Response, expected_code):
        assert response.status_code == expected_code, f"В ответе код {response.status_code} != {expected_code}"

    @staticmethod
    def assert_create_user_with_existing_email(response: Response, error_message):
        assert response.content.decode("utf-8") == error_message, f"Текст сообщения {response.content} != {error_message}"

    @staticmethod
    def assert_invalid_email(response: Response, error_message):
        assert response.content.decode("utf-8") == error_message, f"Текст сообщения {response.content} != {error_message}"

    @staticmethod
    def assert_invalid_parametrs(response: Response, error_message):
        assert response.content.decode("utf-8") == error_message, f"Текст сообщения {response.content} != {error_message}"

    @staticmethod
    def assert_short_name(response: Response, error_message):
        assert response.content.decode("utf-8") == error_message, f"Текст сообщения {response.content} != {error_message}"

    @staticmethod
    def assert_long_name(response: Response, error_message):
        assert response.content.decode("utf-8") == error_message, f"Текст сообщения {response.content} != {error_message}"

    @staticmethod
    def assert_edit_data_without_authorizationh(response: Response, error_message):
        assert response.content.decode("utf-8") == error_message, f"Текст сообщения {response.content} != {error_message}"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:

            assert False, f"Ответ не в формате JSON. Текст '{response.text}'"

        assert name not in response_as_dict, f"В JSON есть ключ '{name}'"

