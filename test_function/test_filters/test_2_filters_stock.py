import pytest
from tools_function.tools import *
import allure



# Для фильтров "Feed Products" и "Published on marketplace"
@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Stock')
@allure.title('Stock')
@allure.severity('critical')
@pytest.mark.parametrize("stock_min, stock_max", [(2, 2), (None, 2), (2, None)])
@pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_stock_feed_pm(representation, stock_min, stock_max):

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
                                                                "stockMin": stock_min,
                                                                "stockMax": stock_max
                                                                },
                                                                "representation": representation
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data']['products']['items']
    assert items_product != [], 'список товаров не должен быть пустым'
    if representation == 'FEED':
        get_check_filters_min_max(items_product, 'stock', stock_min, stock_max, 'на странице "Product feed"')
    elif representation == 'WILDBERRIES':
        get_check_filters_min_max(items_product, 'stock', stock_min, stock_max,
                                  'на странице "Published on marketplace"')


# Для фильтров "Price & Stock rules" / "Business policy"
@allure.epic('Тест стенд v.'+get_app_version())
@allure.feature('Фильтры')
@allure.story('Фильтр по "Stock')
@allure.title('Stock')
@allure.severity('critical')
@pytest.mark.parametrize("stock_min, stock_max", [(2, 2), (None, 2), (2, None)])
@pytest.mark.parametrize("marketplace", ["WILDBERRIES"])
@pytest.mark.parametrize("rule_policy", ["priceStockRuleProducts", "businessPolicyProducts"])
def test_get_filters_stock_rule_policy(rule_policy, marketplace, stock_min, stock_max):

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
                                                                "stockMin": stock_min,
                                                                "stockMax": stock_max
                                                                },
                                                                "marketplace": marketplace
                                                            },
                                                         'query': body})
    response_body = response.json()

    items_product = response_body['data'][rule_policy]['items']
    assert items_product != [], 'список товаров не должен быть пустым'
    get_check_filters_min_max(items_product, 'stock', stock_min, stock_max, 'на странице ' + rule_policy)
