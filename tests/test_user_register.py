import random
import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequest



@allure.epic("Создание пользователя")
class TestUserRegister(BaseCase):
    @allure.title("Позитивный тест на создание пользователя")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_create_user_success(self):
        data = self.prepare_registration_data()
        with allure.step(f"Регистрируемся {register_data}"):
            response = MyRequest.post("/user/", data=data)

        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response, 200)
        with allure.step("Проверяем что в ответе есть ключ id"):
            Assertions.assert_json_has_key(response, "id")


    @allure.title("Тест - пользователь уже существует")
    @allure.severity('CRITICAL')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        with allure.step("Создаем пользователя, который уже есть в системе"):
            response = MyRequest.post("/user/", data=data)

        with allure.step("Проверяем код ответа"):
            Assertions.assert_status_code(response, 400)
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_create_user_with_existing_email(response, f"Users with email '{email}' already exists")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')

    @allure.title("Создание пользователя email невалидный")
    @allure.severity('Minor')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_create_user_invalid_email(self):
        invalid_email = 'zverevexample.com'
        data = self.prepare_registration_data_invaid_email()
        with allure.step("Регистрируемся с невалидным email"):
            response = MyRequest.post("/user/", data=data)
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_invalid_email(response, "Invalid email format")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')

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


    @allure.title("Создание пользователя без обязательных параметров")
    @allure.severity('Minor')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    @pytest.mark.parametrize('data', user1)
    def test_user_no_parameter(self, data):

        d = data
        with allure.step("Регистрация без обязательных параметров"):
            response = MyRequest.post("/user/", data=d)

        if data == self.data_no_all_parameters:
            with allure.step("Проверяем текст сообщения, когда создаём пользователя без всех параметров"):
                Assertions.assert_invalid_parametrs(response, "The following required params are missed: email, password, username, firstName, lastName")
            with allure.step("Сохраняем тело ответа"):
                allure.attach(response.content, 'Response_body')
        elif data == self.data_no_password:
            with allure.step("Проверяем текст сообщения, когда создаём пользователя без пароля"):
                Assertions.assert_invalid_parametrs(response, "The following required params are missed: password")
            with allure.step("Сохраняем тело ответа"):
                allure.attach(response.content, 'Response_body')
        elif data == self.data_no_username:
            with allure.step("Проверяем текст сообщения, когда создаём пользователя без username"):
                Assertions.assert_invalid_parametrs(response, "The following required params are missed: username")
            with allure.step("Сохраняем тело ответа"):
                allure.attach(response.content, 'Response_body')
        elif data == self.data_no_firstName:
            with allure.step("Проверяем текст сообщения, когда создаём пользователя без firstName"):
                Assertions.assert_invalid_parametrs(response, "The following required params are missed: firstName")
            with allure.step("Сохраняем тело ответа"):
                allure.attach(response.content, 'Response_body')
        elif data == self.data_no_lastName:
            with allure.step("Проверяем текст сообщения, когда создаём пользователя без lastName"):
                Assertions.assert_invalid_parametrs(response, "The following required params are missed: lastName")
            with allure.step("Сохраняем тело ответа"):
                allure.attach(response.content, 'Response_body')
        elif data == self.data_no_email:
            with allure.step("Проверяем текст сообщения, когда создаём пользователя без email"):
                Assertions.assert_invalid_parametrs(response, "The following required params are missed: email")
            with allure.step("Сохраняем тело ответа"):
                allure.attach(response.content, 'Response_body')


    @allure.title("Создание пользователя с коротким именем 1 символ")
    @allure.severity('Minor')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_short_name(self):
        data = self.prepare_registration_data()
        username1 = data['username'][:1]
        data['username'] = username1
        #print('prepare_registration_data_short', data)
        '''
        data = {
            'password': '123',
            'username': 'Q',
            'firstName': 'QC',
            'lastName': 'QA/QC',
            'email': self.email
        }
        '''
        with allure.step("Регистрация с коротким именем"):
            response = MyRequest.post("/user/", data=data)
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_short_name(response, "The value of 'username' field is too short")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')

    # Создание пользователя с длинным именем
    @allure.title("Создание пользователя с длинным именем более 255 символов")
    @allure.severity('Minor')
    @allure.issue("https://www.learnqa.ru/")
    @allure.testcase("http://www.testlink.com")
    def test_long_name(self):
        data = self.prepare_registration_data()
        username1 = data['username'][:1]*251
        data['username'] = username1
        #print('prepare_registration_data_long', data)

        '''
        long_name = ''.join(random.choice(string.ascii_lowercase) for i in range(251))
        print(long_name)
    
        data = {
            'password': '123',
            'username': long_name,
            'firstName': 'QC',
            'lastName': 'QA/QC',
            'email': self.email
        }
        '''
        with allure.step("Регистрация длинным именем"):
            response = MyRequest.post("/user/", data=data)
        with allure.step("Проверяем текст сообщения"):
            Assertions.assert_long_name(response, "The value of 'username' field is too long")
        with allure.step("Сохраняем тело ответа"):
            allure.attach(response.content, 'Response_body')
