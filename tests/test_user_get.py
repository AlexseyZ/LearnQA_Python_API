import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequest

class TestUserGet(BaseCase):
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
        response3 = MyRequest.post("/user/login", data=data1)
        # print('данные чужого пользователя -', response3.content)

        # Авторизуюсь под моим пользователем
        response4 = MyRequest.post("/user/login", data=data)
        # Куки для моего пользователя
        auth_sid = self.get_cookie(response4, "auth_sid")
        # Токен для моего пользователя
        token = self.get_header(response4, "x-csrf-token") # токен для моего пользователя
        # id чужого пользователя
        user_id_from_auth_method_no_my_user = self.get_json_value(response3, "user_id")
        # print('чужой id - ', user_id_from_auth_method_no_my_user)

        # Получаю данные с чужим id
        response5 = MyRequest.get(
            f"/user/{user_id_from_auth_method_no_my_user}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        not_expected_fields = ["firstName", "lastName", "email"]
        Assertions.assert_json_has_key(response5, "username")
        Assertions.assert_json_has_not_keys(response5, not_expected_fields)
        # print('запрос со своей куки, но чужим id -', response5.content)


    #Тесты из лекции
    def test_get_user_details_not_auth(self):
        response = MyRequest.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")
        Assertions.assert_json_has_not_key(response, "email")
        #print(response.status_code)
        #print(response.text)

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequest.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")


        response2 = MyRequest.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response2, expected_fields)





