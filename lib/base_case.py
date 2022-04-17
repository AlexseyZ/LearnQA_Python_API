import json.decoder
from requests import Response
from datetime import datetime


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Не удалось найти файл - '{cookie_name}'"
        print(cookie_name)
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Не удалось найти заголовок - '{headers_name}'"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecorder:
            assert False, f"Ответ не в формате JSON. Текст - '{response.text}'"

        assert name in response_as_dict, f"Ответ JSON нет ключа - '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_registration_data_invaid_email(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"

        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

