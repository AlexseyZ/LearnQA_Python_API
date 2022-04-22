import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequest


@allure.epic("Авторизация")
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


        with allure.step("Выполняем авторизацию по логину и паролю"):
            response_1 = MyRequest.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")
        self.user_id_from_auth_method = response_1.json()["user_id"]



    @allure.description("Проверяем, что пользоваетель авторизован")
    @allure.story(f"Тест метода https://playground.learnqa.ru/api/user/auth")
    @allure.title("Позитивный кейс, получаем информацию по авторизованному пользователю")
    @allure.severity('blocker')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_auth_user(self):
        with allure.step("Выполняем запрос на получение информации по авторизованному пользователю"):
            response_2 = MyRequest.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )
        with allure.step("Запрос отправлен, проверим что user_id есть в ответе и он не равен 0"):
            Assertions.assert_json_value_by_name(
                response_2,
                "user_id",
                self.user_id_from_auth_method,
                "Пользователь из метода авторизации не равен пользователю из метода проверки"
        )
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response_2.content, 'Response_body')



    @allure.description("Авторизация только по cookie или только по token")
    @allure.title("Негативный кейс, получаем информацию по авторизованному пользователю только по токену или куки")
    @allure.severity("Minor")
    @pytest.mark.parametrize('condition', params)
    def test_negative(self, condition):

        if condition == "no_cookie":
            with allure.step("Отправляем только токен для авторизации"):
                response_2 = MyRequest.get(
                    "/user/auth",
                    headers={"x-csrf-token": self.token}
                )
        else:
            condition == "no_token"
            with allure.step("Отправляем только cookie для авторизации"):
                response_2 = MyRequest.get(
                    "/user/auth",
                    cookies={"auth_sid": self.auth_sid}
            )
        with allure.step("Запрос отправлен, проверим, что user_id = 0"):
            Assertions.assert_json_value_by_name(
                response_2,
                "user_id",
                0,
                f"Пользователь авторизован {condition}"
            )
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response_2.content, 'Response_body')
            print(response_2.content)

