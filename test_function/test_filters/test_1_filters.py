import pytest
from tools_function.tools import *
import allure

# email = os.environ['EMAIL_SECRET']
# password = os.environ['PASSWORD_SECRET']

def get_check_price(items_product, sale_price_min, sale_price_max):
    count = 0
    for product in items_product:
        if sale_price_min != None and sale_price_max != None:
            count += 1
            print(count, 'salePrice = ', product['salePrice'])
            assert float(product['salePrice']) >= float(sale_price_min) and float(product['salePrice']) <= float(sale_price_max), \
                'проверка цены'
        elif sale_price_min != None:
            count += 1
            print(count, 'salePrice = ', product['salePrice'])
            assert float(product['salePrice']) >= float(sale_price_min), 'проверка цены'
        elif sale_price_max != None:
            count += 1
            print(count, 'salePrice = ', product['salePrice'])
            assert float(product['salePrice']) <= float(sale_price_max), 'проверка цены'


@allure.epic('Тест стенд v.'+get_app_version())
# @allure.feature('Базовое тестирование')
@allure.story('Фильтры')
@allure.title('1) Фильтр по "Sale price"')
@allure.severity('critical')
@pytest.mark.parametrize("action, sale_price_min, sale_price_max",
                         [('price', 100, 100), ('price', None, 100), ('price', 100, None)])
@pytest.mark.parametrize("representation", ["FEED", "WILDBERRIES"])
def test_get_filters_products(action, representation, sale_price_min, sale_price_max):
    print(email)
    print(password)
    # x = open(os.path.join(r"query", "query products (filters).txt"))
    # body = ''.join(x)
    #
    # headers = {"Content-Type": "application/json; charset=utf-8",
    #            "authorization": "JWT " + get_singIn(email, password)}
    # url = get_url()
    # response = requests.post(url, headers=headers, json={'operationName': "products",
    #                                                      'variables': {
    #                                                         "slice": {"offset": 0, "limit": 25},
    #                                                             "pipelineId": 31,
    #                                                             "filters": {
    #                                                             "salePriceMin": sale_price_min,
    #                                                             "salePriceMax": sale_price_max
    #                                                             },
    #                                                             "representation": representation
    #                                                         },
    #                                                      'query': body})
    # response_body = response.json()
    #
    # print()
    # print('Тестовые данные: ')
    # print('salePriceMin =', sale_price_min, ',', 'salePriceMax =', sale_price_max)
    # print('Результат по фильтру:')
    #
    # items_product = response_body['data']['products']['items']
    #
    # if action == 'price':
    #     get_check_price(items_product, sale_price_min, sale_price_max)