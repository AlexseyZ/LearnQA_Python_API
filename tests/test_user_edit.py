import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequest
import allure

@allure.epic("Редактирование пользователя")
class TestUserEdit(BaseCase):
    @allure.title("Позитивный сценарий: регистрация, авторизация, редактирование")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step(f"Регистрируемся {register_data}"):
            response1 = MyRequest.post("/user/", data=register_data)
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response1, 200)
        with allure.step("Проверяем что в ответе есть ключ id"):
            Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        print('login_data- ', login_data)
        with allure.step(f"Авторизация {login_data}"):
            response2 = MyRequest.post("/user/login", data=register_data)
        # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT

        new_name = "Changed name"
        with allure.step(f"Редактируем пользователя {user_id}"):
            response3 = MyRequest.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )
        with allure.step(f"Проверяем код ответа"):
            Assertions.assert_status_code(response3, 200)

        # GET
        with allure.step(f"Получаем данные о пользователя которому изменили имя"):
            response4 = MyRequest.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
        with allure.step(f"Проверям что имя изменилось на {new_name}"):
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Неверное имя пользователя после редактирования"
            )

    @allure.title("Меняем данные неавторизованным пользователем")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_edit_data_without_authorizationh(self):
        new_name2 = "Zverev"
        with allure.step("Выполняем запрос на редактирование без авторизации"):
            response5 = MyRequest.put(
                f"/user/31103",
                data={"firstName": new_name2}
            )
        with allure.step("Проверям код ответа"):
            Assertions.assert_status_code(response5, 400)
        with allure.step("Проверям текст сообщения"):
            Assertions.assert_edit_data_without_authorizationh(response5, 'Auth token not supplied')
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response5.content, 'Response_body')

    @allure.title("Меняем данные под другим пользователем")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_edit_data_under_a_different_user(self):
        register_data = self.prepare_registration_data()
        with allure.step(f"Выполняем регистрацию {register_data}"):
            response1 = MyRequest.post("/user/", data=register_data)
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response1, 200)
        with allure.step("Проверяем что в ответе есть ключ id"):
            Assertions.assert_json_has_key(response1, "id")
        # print(response1.content)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        with allure.step(f"Авторизация {login_data}"):
            response2 = MyRequest.post("/user/login", data=register_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        new_name2 = "Zverev2"
        with allure.step("Редактируем имя чужого пользователя"):
            response3 = MyRequest.put(
                f"/user/31103",
                data={"firstName": new_name2},
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},

            )

        # Методе PUT при редактировании данных под другим пользователем работает неправильно
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response3, 404)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response3.content, 'Response_body')



    @allure.title("Меняем email на невалидный, без символа - @ (авторизованный пользователь)")
    @allure.severity('MINOR')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_edit_invalid_email(self):
        register_data = self.prepare_registration_data()
        with allure.step(f"Выполняем регистрацию {register_data}"):
            response1 = MyRequest.post("/user/", data=register_data)
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response1, 200)
        with allure.step("Проверяем что в ответе есть ключ id"):
            Assertions.assert_json_has_key(response1, "id")


        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        with allure.step(f"Авторизация {login_data}"):
            response2 = MyRequest.post("/user/login", data=register_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        invalid_email = "Zverevexample.com"
        with allure.step(f"Редактируем email {invalid_email}"):
            response3 = MyRequest.put(
                f"/user/31103",
                data={"email": invalid_email},
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},

            )
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response3, 400)
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_invalid_email(response3, 'Invalid email format')

    @allure.title("Меняем имя на короткое - 1 символ (авторизованный пользоваетель)")
    @allure.severity('MINOR')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_edit_short_name(self):
        register_data = self.prepare_registration_data()
        with allure.step(f"Выполняем регистрацию {register_data}"):
            response1 = MyRequest.post("/user/", data=register_data)
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response1, 200)
        with allure.step("Проверяем что в ответе есть ключ id"):
            Assertions.assert_json_has_key(response1, "id")


        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        with allure.step(f"Авторизация {login_data}"):
            response2 = MyRequest.post("/user/login", data=register_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        print(auth_sid)
        print(token)

        short_firstname = "Z"
        with allure.step(f"Меняем на имя содержащие 1 символ {short_firstname}"):
            response3 = MyRequest.put(
                f"/user/31103",
                    data={"firstName": short_firstname},
                    headers={"x-csrf-token": token},
                    cookies={"auth_sid": auth_sid},

            )

        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response3, 400)
        error_message = self.get_json_value(response3, "error")
        with allure.step("Проверяем текст сообщения"):
            assert error_message == "Too short value for field firstName"
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response3.content, 'Response_body')


