import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequest

import allure

@allure.epic("Получение данных о пользователе")
class TestUserGet(BaseCase):
    @allure.title("Авторизовались под одним пользователем, но получает данные другого")
    @allure.severity('Minor')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_get_details_auth_my_user(self):
        data = {
            'email': '1604@qa.com',
            'password': '123'
        }

        # Другой пользователь
        data1 = {
            'email': 'learnqa@04162022163545example.com',
            'password': '123'
        }
        with allure.step("Выполняем авторизацию под пользователем 1"):
            response3 = MyRequest.post("/user/login", data=data1)
        # print('данные чужого пользователя -', response3.content)

        # Авторизуюсь под моим пользователем
        with allure.step("Выполняем авторизацию под пользователем 2"):
            response4 = MyRequest.post("/user/login", data=data)
        # Куки для моего пользователя
        auth_sid = self.get_cookie(response4, "auth_sid")
        # Токен для моего пользователя
        token = self.get_header(response4, "x-csrf-token") # токен для моего пользователя
        # id чужого пользователя
        user_id_from_auth_method_no_my_user = self.get_json_value(response3, "user_id")
        # print('чужой id - ', user_id_from_auth_method_no_my_user)

        # Получаю данные с чужим id
        with allure.step("Получаем данные о пользователе 1 будучи авторизованными по пользователем 2"):
            response5 = MyRequest.get(
                f"/user/{user_id_from_auth_method_no_my_user}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        not_expected_fields = ["firstName", "lastName", "email"]
        with allure.step("Проверяем что в ответе есть ключ username"):
            Assertions.assert_json_has_key(response5, "username")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response5.content, 'Response_body')
        with allure.step(f"Проверям что в ответе не должно быть ключей {not_expected_fields}"):
            Assertions.assert_json_has_not_keys(response5, not_expected_fields)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response5.content, 'Response_body')
        # print('запрос со своей куки, но чужим id -', response5.content)


    #Тесты из лекции
    @allure.title("Получаем информацию о пользователе без авторизации")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_get_user_details_not_auth(self):
        with allure.step("Выполнили запрос только по id"):
            response = MyRequest.get("/user/2")
        with allure.step("Проверям в ответе есть ключ username"):
            Assertions.assert_json_has_key(response, "username")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')
        with allure.step("Проверям в ответе нет ключа firstName"):
            Assertions.assert_json_has_not_key(response, "firstName")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')
        with allure.step("Проверям в ответе нет ключа lastName"):
            Assertions.assert_json_has_not_key(response, "lastName")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')
        with allure.step("Проверям в ответе нет ключа email"):
            Assertions.assert_json_has_not_key(response, "email")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')
        #print(response.status_code)
        #print(response.text)

    @allure.title("Получаем информацию о авторизованным пользователем")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Выполняем авторизацию с данными {data}"):
            response1 = MyRequest.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Выполняем запрос авторизованным пользователем"):
            response2 = MyRequest.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        expected_fields = ["username", "firstName", "lastName", "email"]
        with allure.step(f"Проверяем что в ответе есть ключи {expected_fields}"):
            Assertions.assert_json_has_keys(response2, expected_fields)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response2.content, 'Response_body')






