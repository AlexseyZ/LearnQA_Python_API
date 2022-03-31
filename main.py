import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
response_0 = response.history
response_1 = response.history[0]
response_2 = response.history[1]
response_3 = response.history[2]

print('Количество редиректов -', len(response_0))
print('Начальная точка -', response_1.url)
print('Промежуточная точка -', response_2.url)
print('Конечная точка -', response_3.url)

