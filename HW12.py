import requests


class TestHw12:
    def test_check_headers(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        # Смотрим какие заголовки в ответе
        print('Заголовки -', response.headers)
        print('Значение -', response.headers['x-secret-homework-header'])
        res_headers = response.headers
        res_headers_val = response.headers['x-secret-homework-header']
        #В ответе есть headers:
        assert 'x-secret-homework-header' in response.headers, f"В ответе нет headers {res_headers}"
        #В ответе у headers 'x-secret-homework-header' есть значение:
        assert 'Some secret value' in response.headers['x-secret-homework-header'], f"В ответе у headers нет значения {res_headers_val}"
