from lib.my_requests import MyRequest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    # Пытемся удалить пользователя vinkotov@example.com
    def test_delete_test_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # Логинимся под user_id = 2
        response = MyRequest.post("/user/login", data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")
        # print(auth_sid)
        # print(token)
        # print(user_id)
        # print(response.content)

        # Попытка удалить пользователя под user_id = 2
        response_del = MyRequest.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},

        )

        Assertions.assert_status_code(response_del, 400)
        Assertions.assert_delete_test_user(response_del, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')
        # print(response_del.status_code)
        # print(response_del.content)

    # Создаем и удаляем пользователя, затем проверям, что он действительно удалён
    def test_user_really_deleted(self):
        # Регистрация
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Авторизация
        login = {
            'email': email,
            'password': password
        }

        response2 = MyRequest.post("/user/login", data=login)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаление

        response_del = MyRequest.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},

        )

        Assertions.assert_status_code(response_del, 200)

        # Проверям что пользователь действительно удалён
        response4 = MyRequest.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response4, 404)
        Assertions.assert_get_after_delete(response4, 'User not found')

    # Удалить пользователя, будучи авторизованными другим пользователем
    def test_delete_user_authorized_under_user(self):
        # Регистрация 1 пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']

        # Авторизация 1 пользователя
        login = {
            'email': email,
            'password': password
        }

        response2 = MyRequest.post("/user/login", data=login)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response1, "id")

        Assertions.assert_status_code(response2, 200)

        # print('user_id', user_id)

        # Логинимся под другим пользователем и получаем его id
        data1 = {
            'email': 'learnqa@04162022163545example.com',
            'password': '123'
        }
        response3 = MyRequest.post("/user/login", data=data1)
        user_id2 = self.get_json_value(response3, "user_id")
        # print('user_id2', user_id2)


        # Удаление под другим пользователем
        response_del_under_user = MyRequest.delete(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        # Проверяем, что метод DELETE под другим пользователем отработал неправильно, он удаляет пользователя
        # под которым были авторизованы
        response4 = MyRequest.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response4, 404)
        Assertions.assert_get_after_delete(response4, 'User not found')

        Assertions.assert_status_code(response_del_under_user, 400)














