import pytest
from tools_function.tools import *
import allure


@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Stock')
@allure.title('Stock')
@allure.severity('critical')
@pytest.mark.parametrize("stock_min, stock_max", [(2, 2), (None, 2), (2, None)])
@pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_stock_products(representation, stock_min, stock_max):
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
                                                                "stockMin": stock_min,
                                                                "stockMax": stock_max
                                                                },
                                                                "representation": representation
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data']['products']['items']

    get_check_filters_min_max(items_product, 'stock', stock_min, stock_max, representation)
