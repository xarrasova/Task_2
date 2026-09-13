import allure
import requests
from data import Urls, Headers


@allure.feature('Получение заказов пользователя')
class TestUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_with_auth_success(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}

        response = requests.get(Urls.ORDERS, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["orders"], list)

    @allure.title('Получение заказов без авторизации — ошибка 401')
    def test_get_orders_without_auth_fails(self):
        response = requests.get(Urls.ORDERS, headers=Headers.JSON_HEADERS)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"