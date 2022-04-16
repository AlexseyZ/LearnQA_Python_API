import random
import pytest
import string

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    def setup(self):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}@{random_part}{domain}"
        print('Итоговый email -', self.email)

    # Позитивный тест на создание пользователя
    def test_create_user_success(self):
        data = {
            'password': '123',
            'username': 'ZverevHW16_9',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email

        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        #print('Данные, которые передали для создания пользователя - ', data)
        #print('test_create_user_success', response.content)




        # Проверяем код ответа
        Assertions.assert_status_code(response, 200)
        # Проверяем что в ответе есть ключ id
        Assertions.assert_json_has_key(response, "id")
        # print('Пользователь создан успешно - ', response.content)

    # Тест - пользователь уже существует
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        # Проверяем код ответа
        Assertions.assert_status_code(response, 400)
        # Пользователь уже существует
        Assertions.assert_create_user_with_existing_email(response, f"Users with email '{email}' already exists")

    # Создаем пользователя с  невалидным email
    def test_create_user_invalid_email(self):
        invalid_email = 'zverevexample.com'
        data = {
            'password': '123',
            'username': 'Qa',
            'firstName': 'QC',
            'lastName': 'QA/QC',
            'email': invalid_email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_invalid_email(response, "Invalid email format")

    # Переменные для параметризованного теста
    data_no_password = {
        'username': 'Qa',
        'firstName': 'QC',
        'lastName': 'QA/QC',
        'email': 'zverev' + str(random.randint(0, 999)) + '@ex.com'
    }
    data_no_username = {
        'password': '123',
        'firstName': 'QC',
        'lastName': 'QA/QC',
        'email': 'zverev' + str(random.randint(0, 999)) + '@ex.com'
    }
    data_no_firstName = {
        'password': '123',
        'username': 'Qa',
        'lastName': 'QA/QC',
        'email': 'zverev' + str(random.randint(0, 999)) + '@ex.com'
    }
    data_no_lastName = {
        'password': '123',
        'username': 'Qa',
        'firstName': 'QC',
        'email': 'zverev' + str(random.randint(0, 999)) + '@ex.com'
    }
    data_no_email = {
        'password': '123',
        'username': 'Qa',
        'firstName': 'QC',
        'lastName': 'QA/QC'
    }
    data_no_all_parameters = {}
    user1 = [
        (data_no_all_parameters),
        (data_no_password),
        (data_no_username),
        (data_no_firstName),
        (data_no_lastName),
        (data_no_email)
    ]

    # Создание пользователя без обязательных параметров
    @pytest.mark.parametrize('data', user1)
    def test_user_no_parameter(self, data):
        url = 'https://playground.learnqa.ru/api/user/'
        d = data

        response = requests.post(url, data=d)
        # print(response.content)
        if data == self.data_no_all_parameters:
            Assertions.assert_invalid_parametrs(response, "The following required params are missed: email, password, username, firstName, lastName")
        elif data == self.data_no_password:
            Assertions.assert_invalid_parametrs(response, "The following required params are missed: password")
        elif data == self.data_no_username:
            Assertions.assert_invalid_parametrs(response, "The following required params are missed: username")
        elif data == self.data_no_firstName:
            Assertions.assert_invalid_parametrs(response, "The following required params are missed: firstName")
        elif data == self.data_no_lastName:
            Assertions.assert_invalid_parametrs(response, "The following required params are missed: lastName")
        elif data == self.data_no_email:
            Assertions.assert_invalid_parametrs(response, "The following required params are missed: email")

    # Создание пользователя с коротким именем
    def test_short_name(self):
        data = {
            'password': '123',
            'username': 'Q',
            'firstName': 'QC',
            'lastName': 'QA/QC',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_short_name(response, "The value of 'username' field is too short")

    # Создание пользователя с длинным именем
    def test_long_name(self):
        long_name = ''.join(random.choice(string.ascii_lowercase) for i in range(251))
        # print(long_name)
        data = {
            'password': '123',
            'username': long_name,
            'firstName': 'QC',
            'lastName': 'QA/QC',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_long_name(response, "The value of 'username' field is too long")
        # print("Long name", response.content)
