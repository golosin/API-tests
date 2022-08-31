import requests
import os


# получение url тестируемого стенда
def get_url():
    return 'https://test.app.market4.place/graphql'


# получение id пайплайна
def get_id_pipeline():
    return 1


# SingIn (авторизация и получение токена)
def get_singIn():
    email = os.environ['EMAIL_SECRET']
    password = os.environ['PASSWORD_SECRET']

    x = open(os.path.join(r"query", "mutation SignInMutation.txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = get_url()
    response = requests.post(url, headers=headers, json={'operationName': "SignInMutation",
                                                                     'variables': {'email': email,
                                                                                   'password': password},
                                                                     'query': body})
    response_body = response.json()
    return response_body['data']['signIn']['token']


# Версия билда
def get_app_version():
    x = open(os.path.join(r"query", "query appVersion.txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "authorization": "JWT " + get_singIn()}
    url = get_url()
    response = requests.post(url, headers=headers, json={'query': body})
    response_body = response.json()
    return response_body['data']['appVersion']['appVersion']


# Проверка попадания в диапазон значений для двух параметров
def get_check_filters_min_max(items_product, type, min_value, max_value, discription):
    count = 0
    print()
    print('Тестовые данные:', type)
    print('min =', min_value, ',', 'max =', max_value)
    print('Результат по фильтру: ' + discription)
    for product in items_product:

        value = str(product[type])
        if '-' in value:
            value = ''.join(value.split('-')[:-1])

        if min_value != None and max_value != None:
            count += 1
            print(count, type, '=', value)
            assert float(value) >= float(min_value) and float(value) <= float(max_value), \
                'проверка ' + type
        elif min_value != None:
            count += 1
            print(count, type, '=', value)
            assert float(value) >= float(min_value), 'проверка ' + type
        elif max_value != None:
            count += 1
            print(count, type, '=', value)
            assert float(value) <= float(max_value), 'проверка ' + type


# Проверка булёвого значения
def get_check_filters_value_with_checkvalue(items_product, type, value, check_value, discription):
    count = 0
    print()
    print('Тестовые данные:', type)
    print(type, '=', value)
    print('Результат по фильтру: ' + discription)
    for product in items_product:
        if value == check_value:
            count += 1
            print(count, type, '=', product[type])
            assert product[type] == check_value, 'проверка ' + type
        elif value != check_value:
            count += 1
            print(count, type, '=', product[type])
            assert product[type] != check_value, 'проверка ' + type