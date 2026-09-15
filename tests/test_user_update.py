import allure
import requests

from data import Urls, Headers
from helpers import generate_random_user


@allure.feature('Изменение данных пользователя')
class TestUserUpdate:

    @allure.title('Изменение имени пользователя с авторизацией')
    def test_update_user_name_with_auth_success(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}
        new_value = "Updated_Name"

        with allure.step("Отправить PATCH-запрос на изменение имени"):
            response = requests.patch(Urls.USER, json={"name": new_value}, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == new_value

    @allure.title('Изменение email пользователя с авторизацией')
    def test_update_user_email_with_auth_success(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}
        new_value = generate_random_user()["email"]

        with allure.step("Отправить PATCH-запрос на изменение email"):
            response = requests.patch(Urls.USER, json={"email": new_value}, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == new_value

    @allure.title('Изменение пароля пользователя с авторизацией')
    def test_update_user_password_with_auth_success(self, create_user):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}
        new_value = "new_password_123"

        with allure.step("Отправить PATCH-запрос на изменение пароля"):
            response = requests.patch(Urls.USER, json={"password": new_value}, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Изменение данных без авторизации — ошибка 401')
    def test_update_user_without_auth_fails(self):
        update_payload = {"name": "Updated_Name"}

        with allure.step("Отправить PATCH-запрос без авторизации"):
            response = requests.patch(Urls.USER, json=update_payload, headers=Headers.JSON_HEADERS)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"