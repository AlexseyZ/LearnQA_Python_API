import requests
import time
import json

#Отладка
#Запрос без GET - параметра
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print('Ответ без get параметра -', response.text)
#Запрос c GET-параметром token (валидный)
jbget_Val= {"token":"gNzoDOzoDNxAyMw0CNw0iMyAjM"}#валидный
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=jbget_Val)
print('Ответ на валидный токен  -', response.text)
#Запрос c GET-параметром token (невалидный)
jbget_Nval= {"token":"gNzoDOzoDNxAyMw0CNw0iMyA88jM"}#невалидный
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=jbget_Nval)
print('Ответ на невалидный токен  -', response.text)



#1.Cоздаем задачу
response_create_job = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

#Парсим json и достаем значение токена
response_parse = response_create_job.json()
token_p = response_parse["token"]
#Записываем токен в переменную
token_job = {"token": token_p}
#Получаем время через которое будет готова задача
time_job = response_parse["seconds"]
#2.Проверяем статус
response_status = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token_job)
response_parse_status = response_status.json()#парсим ответ
status = response_parse_status["status"]# получаем значение ключа status

if status == "Job is NOT ready":
    print("Задача пока не готова - ОК, ожидаем")
    time.sleep(time_job)
elif status == "Job is ready":
    print("Задача готова")

#3.Делаем запрос после готовности задачи
response_result_status = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token_job)

response_parse_result_status = response_result_status.json()
response_status_result_ready = response_parse_result_status["status"]
key = "result"
if response_status_result_ready == "Job is ready" and key in response_parse_result_status:
    print('В ответе есть ключ - result и поле статус содержит текст - Job is ready')
else:
    print("Что-то пошло не так")