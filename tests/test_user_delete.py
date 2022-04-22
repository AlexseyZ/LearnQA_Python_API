from lib.my_requests import MyRequest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Удаление пользователя")
class TestUserDelete(BaseCase):
    # Пытемся удалить пользователя vinkotov@example.com
    @allure.title("Пытемся удалить пользователя vinkotov@example.com")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_delete_test_user(self):
        user = 'vinkotov@example.com'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Логинимся под пользовтелем {user}"):
            response = MyRequest.post("/user/login", data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")
        # print(auth_sid)
        # print(token)
        # print(user_id)
        # print(response.content)

        # Попытка удалить пользователя под user_id = 2
        with allure.step(f"Удаляем пользователя - {user}"):
            response_del = MyRequest.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response_del, 400)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response_del.status_code, 'Response_body')
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_delete_test_user(response_del, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response_del.content, 'Response_body')

    # Создаем и удаляем пользователя, затем проверям, что он действительно удалён
    @allure.title("Создаем и удаляем пользователя, затем проверям, что он действительно удалён")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_user_really_deleted(self):
        # Регистрация
        register_data = self.prepare_registration_data()
        with allure.step(f"Выполняем регистрацию с данными {register_data}"):
            response1 = MyRequest.post("/user/", data=register_data)
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response1, 200)
        with allure.step("Проверяем ключ id в ответе"):
            Assertions.assert_json_has_key(response1, "id")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Авторизация
        login = {
            'email': email,
            'password': password
        }
        with allure.step(f"Авторизуемся {login}"):
            response2 = MyRequest.post("/user/login", data=login)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаление
        with allure.step(f"Удаляем пользоватея {user_id}"):
            response_del = MyRequest.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},

            )
        with allure.step(f"Проверяем код ответа"):
            Assertions.assert_status_code(response_del, 200)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')

        # Проверям что пользователь действительно удалён
        with allure.step(f"Проверяем что пользоваетель удалён {user_id}"):
            response4 = MyRequest.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response4, 404)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_get_after_delete(response4, 'User not found')
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')

    # Удалить пользователя, будучи авторизованными другим пользователем
    @allure.title("Удалить пользователя, будучи авторизованными другим пользователем")
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_delete_user_authorized_under_user(self):
        # Регистрация 1 пользователя
        register_data = self.prepare_registration_data()
        with allure.step(f"Выполняем регистрацию с данными {register_data}"):
            response1 = MyRequest.post("/user/", data=register_data)
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response1, 200)
        with allure.step("Проверяем ключ id в ответе"):
            Assertions.assert_json_has_key(response1, "id")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']

        # Авторизация 1 пользователя
        login = {
            'email': email,
            'password': password
        }
        with allure.step(f"Авторизуемся {login}"):
            response2 = MyRequest.post("/user/login", data=login)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response1, "id")
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response2, 200)

        # print('user_id', user_id)

        # Логинимся под другим пользователем и получаем его id
        data1 = {
            'email': 'learnqa@04162022163545example.com',
            'password': '123'
        }
        with allure.step(f"Авторизуемся под другим пользователем - {data1}"):
            response3 = MyRequest.post("/user/login", data=data1)
        user_id2 = self.get_json_value(response3, "user_id")
        # print('user_id2', user_id2)


        # Удаление под другим пользователем
        with allure.step(f"Удаляем пользоватля 1 под пользователем 2 - {user_id2}"):
            response_del_under_user = MyRequest.delete(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        # Проверяем, что метод DELETE под другим пользователем отработал неправильно, он удаляет пользователя
        # под которым были авторизованы
        with allure.step(f"Проверяем, что метод DELETE под другим пользователем отработал неправильно"):
            response4 = MyRequest.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response4, 404)
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_get_after_delete(response4, 'User not found')
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')
        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response_del_under_user, 400)
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response1.content, 'Response_body')














