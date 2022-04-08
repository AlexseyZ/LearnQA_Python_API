import requests


class TestHw11:
    def test_check_cookies(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        #Смотрим какие cookies в ответе
        print('Cookies -', response.cookies)
        print('Значение -', response.cookies['HomeWork'])
        res_cook = response.cookies
        res_cook_val = response.cookies['HomeWork']
        #В ответе есть cookie:
        assert 'HomeWork' in response.cookies, f"В ответе нет cookie {res_cook}"
        # В ответе у cookie 'HomeWork' есть значение:
        assert 'hw_value' in response.cookies['HomeWork'], f"В ответе у cookie нет значения {res_cook_val}"




