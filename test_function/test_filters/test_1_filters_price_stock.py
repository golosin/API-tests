import pytest
from tools_function.tools import *
import allure


def get_check_price_stock(items_product, type, min_value, max_value, representation):
    count = 0
    print()
    print('Тестовые данные:', type)
    print('min =', min_value, ',', 'max =', max_value)
    print('Результат по фильтру: ' + representation)
    for product in items_product:
        if min_value != None and max_value != None:
            count += 1
            print(count, type, '=', product[type])
            assert float(product[type]) >= float(min_value) and float(product[type]) <= float(max_value), \
                'проверка ' + type
        elif min_value != None:
            count += 1
            print(count, type, '=', product[type])
            assert float(product[type]) >= float(min_value), 'проверка ' + type
        elif max_value != None:
            count += 1
            print(count, type, '=', product[type])
            assert float(product[type]) <= float(max_value), 'проверка ' + type


@allure.epic('Тест стенд v.'+get_app_version())
# @allure.feature('Базовое тестирование')
@allure.story('Фильтры')
@allure.title('1) Фильтр по "Sale price"/"Stock"')
@allure.severity('critical')
@pytest.mark.parametrize("action, sale_price_min, sale_price_max, stock_min, stock_max",
                         [('price', 100, 100, None, None), ('price', None, 100, None, None), ('price', 100, None, None, None),
                          ('stock', None, None, 2, 2), ('stock', None, None, None, 2), ('stock', None, None, 2, None)])
@pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_price_stock_products(action, representation, sale_price_min, sale_price_max, stock_min, stock_max):
    x = open(os.path.join(r"query", "query products (filters).txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "authorization": "JWT " + get_singIn()}
    url = get_url()
    response = requests.post(url, headers=headers, json={'operationName': "products",
                                                         'variables': {
                                                            "slice": {"offset": 0, "limit": 25},
                                                                "pipelineId": 31,
                                                                "filters": {
                                                                "salePriceMin": sale_price_min,
                                                                "salePriceMax": sale_price_max,
                                                                "stockMin": stock_min,
                                                                "stockMax": stock_max
                                                                },
                                                                "representation": representation
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data']['products']['items']

    if action == 'price':
        get_check_price_stock(items_product, 'salePrice', sale_price_min, sale_price_max, representation)
    elif action == 'stock':
        get_check_price_stock(items_product, 'stock', stock_min, stock_max, representation)
