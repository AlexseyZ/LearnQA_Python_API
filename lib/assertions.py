from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(responce: Response, name, expected_value, error_message):
        try:
            response_as_dict = responce.json()
        except json.JSONDecodeError:

            assert False, f"Ответ не в формате JSON. Текст '{response.text}'"

        assert name in response_as_dict, f"Ответ JSON нет ключа  '{name}'"
        assert response_as_dict[name] == expected_value, error_message