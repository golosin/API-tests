import requests
import os


# получение url тестируемого стенда
def get_url():
    return 'https://test.app.market4.place/graphql'


# SingIn (авторизация и получение токена)
def get_singIn(email, password):
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
               "authorization": "JWT " + get_singIn("testadmin@t4mp.com", "9hm2wAg8rDzP2kn")}
    url = get_url()
    response = requests.post(url, headers=headers, json={'query': body})
    response_body = response.json()
    return response_body['data']['appVersion']['appVersion']