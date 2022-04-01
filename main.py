import requests
method_get = {"method": "GET"}
method_post = {"method": "POST"}
method_delete = {"method": "DELETE"}
method_put = {"method": "PUT"}
method_head = {"method": "HEAD"}# метод не из списка

#http-запрос любого типа без параметра method
r = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type')
print('Запрос без параметра -', r.text)

# http-запрос не из списка. Например, HEAD
r1 = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_head)
print('Запрос не из списка -', r1.text)

# http-запрос с правильным значением method
r2 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=method_get)
print('Запрос с правильным method -', r2.text)

# Создаем переменные в различных комбинациях
print('GET ##########################')
get_get = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=method_get)
print('Ответ get_get -', get_get.text)
get_post = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=method_post)
print('Ответ get_post -', get_post.text)
get_delete = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=method_delete)
print('Ответ get_delete -', get_delete.text)
get_put = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=method_put)
print('Ответ get_put -', get_put.text)
print('POST ##########################')
post_post = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_post)
print('Ответ post_post -', post_post.text)
post_get = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_get)
print('Ответ post_get -', post_get.text)
post_delete = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_delete)
print('Ответ post_delete -', post_delete.text)
post_put = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_put)
print('Ответ post_put -', post_put.text)
print('DELETE ##########################')
delete_delete = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_delete)
print('Ответ delete_delete -', delete_delete.text)
delete_get = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_get)
print('Ответ delete_get -', delete_get.text)
delete_post = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_post)
print('Ответ delete_post -', delete_post.text)
delete_put = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_put)
print('Ответ delete_put -', delete_put.text)
print('PUT ##########################')
put_put = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_put)
print('Ответ put_put -', put_put.text)
put_get = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_get)
print('Ответ put_get -', put_get.text)
put_post = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_post)
print('Ответ put_post -', put_post.text)
put_delete = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data=method_delete)
print('Ответ put_delete-', put_delete.text)



print('Проверяем метод GET')
s = '{"success":"!"}'
if get_get.text == s:
    print('get_get - ОК')
else:
    print('get_get - FAIL')
if get_post.text != s:
    print('get_post - ОК')
else:
    print('get_post - FAIL')
if get_delete.text != s:
    print('get_delete - ОК')
else:
    print('get_delete - FAIL')
if get_put.text != s:
    print('get_put - ОК')
else:
    print('get_put - FAIL')
print('Проверяем метод POST')
if post_post.text == s:
    print('post_post - ОК')
else:
    print('post_post - FAIL')
if post_get.text != s:
    print('post_get - ОК')
else:
    print('post_get - FAIL')
if post_put.text != s:
    print('post_put - ОК')
else:
    print('post_put - FAIL')
if post_delete.text != s:
    print('post_delete - ОК')
else:
    print('post_delete - FAIL')
print('Проверяем метод PUT')
if put_put.text == s:
    print('put_put - ОК')
else:
    print('put_put - FAIL')
if put_get.text != s:
    print('put_get - ОК')
else:
    print('put_get - FAIL')
if put_post.text != s:
    print('put_post - ОК')
else:
    print('put_post - FAIL')
if put_delete.text != s:
    print('put_delete - ОК')
else:
    print('put_delete - FAIL')
print('Проверяем метод DELETE')
if delete_delete.text == s:
    print('delete_delete - ОК')
else:
    print('delete_delete - FAIL')
if delete_post.text != s:
    print('delete_post - ОК')
else:
    print('delete_post - FAIL')
if delete_get.text != s:
    print('delete_get - ОК')
else:
    print('delete_get - FAIL')
if delete_put.text != s:
    print('delete_put - ОК')
else:
    print('delete_put - FAIL')