import pytest
from tools_function.tools import *
import allure


@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Sale price"')
@allure.title('Sale price')
@allure.severity('critical')
@pytest.mark.parametrize("sale_price_min, sale_price_max", [(100, 100), (None, 100), (100, None)])
@pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_price_products(representation, sale_price_min, sale_price_max):
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
                                                                "salePriceMax": sale_price_max
                                                                },
                                                                "representation": representation
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data']['products']['items']

    get_check_filters_min_max(items_product, 'salePrice', sale_price_min, sale_price_max, representation)

