import allure
import pytest
import requests

from data import Urls, Headers
from helpers import generate_random_user


@allure.feature('Создание пользователя')
class TestUserCreation:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user_success(self, create_user):
        response = create_user["response"]
        payload = create_user["payload"]

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == payload["email"]
        assert response.json()["user"]["name"] == payload["name"]

    @allure.title('Создание пользователя, который уже зарегистрирован — ошибка 403')
    def test_create_duplicate_user_fails(self, create_user):
        existing_payload = create_user["payload"]

        with allure.step("Отправить POST-запрос на регистрацию с существующими данными"):
            response = requests.post(Urls.REGISTER, json=existing_payload, headers=Headers.JSON_HEADERS)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "User already exists"

    @allure.title('Создание пользователя без одного из обязательных полей — ошибка 403')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field_fails(self, missing_field):
        payload = generate_random_user()
        payload.pop(missing_field)

        with allure.step(f"Отправить POST-запрос без поля {missing_field}"):
            response = requests.post(Urls.REGISTER, json=payload, headers=Headers.JSON_HEADERS)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"