import allure
import requests

from data import Urls, Headers
from helpers import get_valid_ingredient_ids


@allure.feature('Создание заказа')
class TestOrderCreation:

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_auth_success(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}
        valid_ids = get_valid_ingredient_ids(count=2)

        with allure.step("Отправить POST-запрос на создание заказа с авторизацией"):
            response = requests.post(Urls.ORDERS, json={"ingredients": valid_ids}, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["order"]["number"] is not None

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth_success(self):
        valid_ids = get_valid_ingredient_ids(count=2)

        with allure.step("Отправить POST-запрос на создание заказа без авторизации"):
            response = requests.post(Urls.ORDERS, json={"ingredients": valid_ids}, headers=Headers.JSON_HEADERS)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["order"]["number"] is not None

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients_success(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}
        valid_ids = get_valid_ingredient_ids(count=2)

        with allure.step("Отправить POST-запрос с ингредиентами"):
            response = requests.post(Urls.ORDERS, json={"ingredients": valid_ids}, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Создание заказа без ингредиентов — ошибка 400')
    def test_create_order_without_ingredients_fails(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}

        with allure.step("Отправить POST-запрос с пустым массивом ингредиентов"):
            response = requests.post(Urls.ORDERS, json={"ingredients": []}, headers=headers)

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title('Создание заказа с неверным хешем ингредиентов — ошибка 500')
    def test_create_order_with_invalid_ingredient_fails(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}

        with allure.step("Отправить POST-запрос с неверным хешем"):
            response = requests.post(Urls.ORDERS, json={"ingredients": ["invalid_hash_12345"]}, headers=headers)

        assert response.status_code == 500