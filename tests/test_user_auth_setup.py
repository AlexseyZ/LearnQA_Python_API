import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")
        # assert "auth_sid" in response_1.cookies, "В ответе нет куки auth_sid"
        # assert "x-csrf-token" in response_1.headers, "В ответе нет токена x-csrf-token"
        # assert "user_id" in response_1.json(), "В ответе нет user_id"

        # self.auth_sid = response_1.cookies.get("auth_sid")
        # self.token = response_1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response_1.json()["user_id"]
        # print('Куки из ответа после авторизации -', self.auth_sid)
        # print('Токен из ответа после авторизации -', self.token)
        print('user_id из ответа после авторизации -', self.user_id_from_auth_method)

    def test_auth_user(self):
        response_2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response_2,
            "user_id",
            self.user_id_from_auth_method,
            "Пользователь из метода авторизации не равен пользователю из метода проверки"
        )

        # assert "user_id" in response_2.json(), "Во втором ответе нет user_id"
        # user_id_from_check_method = response_2.json()["user_id"]

        # assert self.user_id_from_auth_method == user_id_from_check_method, f"Пользователь из метода авторизации не " \
        # f"равен пользователю из метода проверки "

    @pytest.mark.parametrize('condition', params)
    def test_negative(self, condition):

        if condition == "no_cookie":
            response_2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            condition == "no_token"
            response_2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )
        Assertions.assert_json_value_by_name(
            response_2,
            "user_id",
            0,
            f"Пользователь авторизован {condition}"
        )

        # assert "user_id" in response_2.json(), "Во втором ответе нет user_id"

        # user_id_from_check_method = response_2.json()["user_id"]
        # print('user_id_from_check_method - ', user_id_from_check_method)

        # assert user_id_from_check_method == 0, f"Пользователь авторизован {condition}"
