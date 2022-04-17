import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequest


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        #response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        print(response1.content)

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

        response2 = MyRequest.post("/user/login", data=register_data)
        # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT

        new_name = "Changed name"

        response3 = MyRequest.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response3, 200)

        # GET

        response4 = MyRequest.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Неверное имя пользователя после редактирования"
        )

    # Меняем данные неавторизованным пользователем

    def test_edit_data_without_authorizationh(self):
        new_name2 = "Zverev"
        response5 = MyRequest.put(
            f"/user/31103",
            data={"firstName": new_name2}
        )

        Assertions.assert_status_code(response5, 400)
        Assertions.assert_edit_data_without_authorizationh(response5, 'Auth token not supplied')

        print(response5.status_code)

        print('test_edit_user_no_auth - ', response5.content)


    # Меняем данные под другим пользователем

    def test_edit_data_under_a_different_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        # response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
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

        print('login_data- ', login_data)

        response2 = MyRequest.post("/user/login", data=register_data)
        #response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        print('response2', response2.content)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        print(auth_sid)
        print(token)

        new_name2 = "Zverev2"
        response3 = MyRequest.put(
            f"/user/31103",
            data={"firstName": new_name2},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},

        )
        # print('response3', response3.status_code)
        # print('test_edit_data_under_a_different_user', response3.content)

        # Методе PUT при редактировании данных под другим пользователем работает неправильно
        Assertions.assert_status_code(response3, 404)

    # Меняем email на невалидный, без символа - @ (авторизованный пользователь)
    def test_edit_invalid_email(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        # response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
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

        print('login_data- ', login_data)

        response2 = MyRequest.post("/user/login", data=register_data)
        # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        print('response2', response2.content)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        # print(auth_sid)
        # print(token)

        invalid_email = "Zverevexample.com"
        response3 = MyRequest.put(
            f"/user/31103",
            data={"email": invalid_email},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},

        )
        #print('response3', response3.status_code)
        #print('test_edit_invalid', response3.content)

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_invalid_email(response3, 'Invalid email format')

    # Меняем имя на короткое (авторизованный пользоваетель)
    def test_edit_short_name(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        # response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
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

        print('login_data- ', login_data)

        response2 = MyRequest.post("/user/login", data=register_data)
        # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        print('response2', response2.content)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        print(auth_sid)
        print(token)

        short_firstname = "Z"
        response3 = MyRequest.put(
            f"/user/31103",
            data={"firstName": short_firstname},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},

        )
        print('response3', response3.status_code)
        print('short_name', response3.content)

        Assertions.assert_status_code(response3, 400)
        error_message = self.get_json_value(response3, "error")
        assert error_message == "Too short value for field firstName"


