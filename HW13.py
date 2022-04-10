import requests
import pytest
import json


##Отладка
#Агент - 1
User_Agent1 = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
response1 = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=User_Agent1)
response_js_1 = response1.json()
print(response1.text)
print('Platform_1 -', response_js_1["platform"])
print('Browser_1 -', response_js_1["browser"])
print('Device_1 -', response_js_1["device"])
print('******************')
#Агент - 2
User_Agent2 = {'User-Agent':'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'}
response2 = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=User_Agent2)
response_js_2 = response2.json()
print(response2.text)
print('Platform_2 -', response_js_2["platform"])
print('Browser_2 -', response_js_2["browser"])
print('Device_2 -', response_js_2["device"])
print('******************')
#Агент - 3
User_Agent3 = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
response3 = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=User_Agent3)
response_js_3 = response3.json()
print(response3.text)
print('Platform_3 -', response_js_3["platform"])
print('Browser_3 -', response_js_3["browser"])
print('Device_3 -', response_js_3["device"])
print('******************')
#Агент - 4
User_Agent4 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'}
response4 = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=User_Agent4)
response_js_4 = response4.json()
print(response4.text)
print('Platform_4 -', response_js_4["platform"])
print('Browser_4 -', response_js_4["browser"])
print('Device_4 -', response_js_4["device"])
print('******************')
#Агент - 5
User_Agent5 = {'User-Agent':'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
response5 = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=User_Agent5)
response_js_5 = response5.json()
print(response5.text)
print('Platform_5 -', response_js_5["platform"])
print('Browser_5 -', response_js_5["browser"])
print('Device_5 -', response_js_5["device"])



class TestHw13:
    User_Agent_var = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30")
        ,
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]

    @pytest.mark.parametrize('agent', User_Agent_var)
    def test_user_agent(self, agent):
        url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'
        h = {'User-Agent': agent}
        response = requests.get(url, headers=h)
        response_js = response.json()
        #Фактический результат
        actual_responce_platform = response_js["platform"]
        actual_responce_browser = response_js["browser"]
        actual_responce_device = response_js["device"]
        #Ожидаемый результат
        expected_platform1 = 'Mobile'
        expected_browser1 = 'No'
        expected_device1 = 'Android'

        expected_platform2 = 'Mobile'
        expected_browser2 = 'Chrome'
        expected_device2 = 'iOS'

        expected_platform3 = 'Googlebot'
        expected_browser3 = 'Unknown'
        expected_device3 = 'Unknown'

        expected_platform4 = 'Web'
        expected_browser4 = 'Chrome'
        expected_device4 = 'No'

        expected_platform5 = 'Mobile'
        expected_browser5 = 'No'
        expected_device5 = 'iPhone'


        if h == User_Agent1:
            assert actual_responce_platform == expected_platform1, f"Не та платформа - {actual_responce_platform},ожидали - {expected_platform1} "
            assert actual_responce_browser == expected_browser1, f"Не тот браузер - {actual_responce_browser}, ожидали - {expected_browser1} "
            assert actual_responce_device == expected_device1, f"Не то устройство - {actual_responce_device}, ожидали - {expected_device1} "
        elif h == User_Agent2:
            assert actual_responce_platform == expected_platform2, f"Не та платформа - {actual_responce_platform},ожидали - {expected_platform2} "
            assert actual_responce_browser == expected_browser2, f"Не тот браузер - {actual_responce_browser}, ожидали - {expected_browser2} "
            assert actual_responce_device == expected_device2, f"Не то устройство - {actual_responce_device}, ожидали - {expected_platform2} "
        elif h == User_Agent3:
            assert actual_responce_platform == expected_platform3, f"Не та платформа - {actual_responce_platform},ожидали - {expected_platform3} "
            assert actual_responce_browser == expected_browser3, f"Не тот браузер - {actual_responce_browser}, ожидали - {expected_browser3} "
            assert actual_responce_device == expected_device3, f"Не то устройство - {actual_responce_device}, ожидали - {expected_platform3} "
        elif h == User_Agent4:
            assert actual_responce_platform == expected_platform4, f"Не та платформа - {actual_responce_platform},ожидали - {expected_platform4} "
            assert actual_responce_browser == expected_browser4, f"Не тот браузер - {actual_responce_browser}, ожидали - {expected_browser4} "
            assert actual_responce_device == expected_device4, f"Не то устройство - {actual_responce_device}, ожидали - {expected_platform4} "
        elif h == User_Agent5:
            assert actual_responce_platform == expected_platform5, f"Не та платформа - {actual_responce_platform},ожидали - {expected_platform5} "
            assert actual_responce_browser == expected_browser5, f"Не тот браузер - {actual_responce_browser}, ожидали - {expected_browser5} "
            assert actual_responce_device == expected_device5, f"Не то устройство - {actual_responce_device}, ожидали - {expected_platform5} "

