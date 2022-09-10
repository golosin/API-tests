import pytest
from tools_function.tools import *
import allure


# Для фильтров "Feed Products" и "Published on marketplace"
@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Sale price"')
@allure.title('Sale price')
@allure.severity('critical')
@pytest.mark.parametrize("sale_price_min, sale_price_max", [(100, 100), (None, 100), (100, None)])
# @pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_price_feed_pm(representation, sale_price_min, sale_price_max):


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
                                                                "salePriceMin": sale_price_min,
                                                                "salePriceMax": sale_price_max
                                                                },
                                                                "representation": representation
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data']['products']['items']
    assert items_product != [], 'список товаров не должен быть пустым'
    if representation == 'FEED':
        get_check_filters_min_max(items_product, 'salePrice', sale_price_min, sale_price_max,
                                  'на странице "Product feed"')
    elif representation == 'WILDBERRIES':
        get_check_filters_min_max(items_product, 'salePrice', sale_price_min, sale_price_max,
                                  'на странице "Published on marketplace"')


# Для фильтров "Price & Stock rules" / "Business policy"
@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Sale price"')
@allure.title('Sale price')
@allure.severity('critical')
@pytest.mark.parametrize("sale_price_min, sale_price_max", [(100, 100), (None, 100), (100, None)])
@pytest.mark.parametrize("marketplace", ["WILDBERRIES"])
@pytest.mark.parametrize("rule_policy", ["priceStockRuleProducts", "businessPolicyProducts"])
def test_get_filters_price_rule_policy(rule_policy, marketplace, sale_price_min, sale_price_max):

    x = open(os.path.join(r"query", "query " + rule_policy + ".txt"))
    body = ''.join(x)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "authorization": "JWT " + get_singIn()}
    url = get_url()
    response = requests.post(url, headers=headers, json={'operationName': rule_policy,
                                                         'variables': {
                                                            "slice": {"offset": 0, "limit": 25},
                                                                "pipelineId": get_id_pipeline(),
                                                                "filters": {
                                                                "salePriceMin": sale_price_min,
                                                                "salePriceMax": sale_price_max
                                                                },
                                                                "marketplace": marketplace
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data'][rule_policy]['items']
    assert items_product != [], 'список товаров не должен быть пустым'
    get_check_filters_min_max(items_product, 'salePrice', sale_price_min, sale_price_max, 'на странице ' + rule_policy)
