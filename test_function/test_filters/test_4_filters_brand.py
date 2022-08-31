import pytest
from tools_function.tools import *
import allure

# Для фильтров "Feed Products" и "Published on marketplace"
@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Brand"')
@allure.title('Brand')
@allure.severity('critical')
@pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_brand_feed_pm(representation):

    x = open(os.path.join(r"query", "query products.txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "authorization": "JWT " + get_singIn()}
    url = get_url()
    response = requests.post(url, headers=headers, json={'operationName': "products",
                                                         'variables': {
                                                            "slice": {"offset": 0, "limit": 25},
                                                                "pipelineId": get_id_pipeline(),
                                                                "representation": representation
                                                            },
                                                         'query': body})
    response_body = response.json()
    if representation == 'FEED':
        token_brand = response_body['data']['products']['pageInfo']['filters'][15]['widget']['attrs'][0]['value']
    elif representation == 'WILDBERRIES':
        token_brand = response_body['data']['products']['pageInfo']['filters'][18]['widget']['attrs'][0]['value']


    x = open(os.path.join(r"query", "query DictionaryOptionsQuery.txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "authorization": "JWT " + get_singIn()}
    url = get_url()
    response = requests.post(url, headers=headers, json={'operationName': "DictionaryOptionsQuery",
                                                         'variables': {
                                                             "slice": {"offset": 0, "limit": 25},
                                                             "pipelineId": get_id_pipeline(),
                                                             "token": token_brand
                                                         },
                                                         'query': body})
    response_body = response.json()
    brand = response_body['data']['dictionaryOptions'][0]['value']



    x = open(os.path.join(r"query", "query products.txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "authorization": "JWT " + get_singIn()}
    url = get_url()
    response = requests.post(url, headers=headers, json={'operationName': "products",
                                                         'variables': {
                                                             "slice": {"offset": 0, "limit": 25},
                                                             "pipelineId": get_id_pipeline(),
                                                             "filters": {
                                                                 "brand": brand
                                                             },
                                                             "representation": representation
                                                         },
                                                         'query': body})
    response_body = response.json()
    items_product = response_body['data']['products']['items']

    if representation == 'FEED':
        get_check_filters_value_with_checkvalue(items_product, 'brand', brand, brand, 'на странице "Product feed"')
    elif representation == 'WILDBERRIES':
        get_check_filters_value_with_checkvalue(items_product, 'brand', brand, brand,
                                                'на странице "Published on marketplace"')