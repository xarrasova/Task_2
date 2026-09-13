import allure
import requests
from data import Urls, Headers
from helpers import generate_random_user


@allure.feature('Логин пользователя')
class TestUserLogin:

    @allure.title('Логин под существующим пользователем')
    def test_login_existing_user_success(self, create_user):
        payload = create_user["payload"]
        response = requests.post(Urls.LOGIN, json=payload, headers=Headers.JSON_HEADERS)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == payload["email"]
        assert response.json()["accessToken"] is not None

    @allure.title('Логин с неверным логином и паролем — ошибка 401')
    def test_login_with_wrong_credentials_fails(self):
        # Сгенерированные, но НЕ зарегистрированные данные
        payload = generate_random_user()
        response = requests.post(Urls.LOGIN, json=payload, headers=Headers.JSON_HEADERS)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"