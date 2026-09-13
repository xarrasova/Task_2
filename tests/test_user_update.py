import allure
import pytest
import requests
from data import Urls, Headers
from helpers import generate_random_user


@allure.feature('Изменение данных пользователя')
class TestUserUpdate:

    @allure.title('Изменение поля {field} с авторизацией')
    @pytest.mark.parametrize("field", ["name", "email", "password"])
    def test_update_user_with_auth_success(self, create_user, field):
        token = create_user["token"]
        headers = {"Authorization": token, **Headers.JSON_HEADERS}

        if field == "name":
            new_value = "Updated_Name"
        elif field == "email":
            new_value = generate_random_user()["email"]
        else:
            new_value = "new_password_123"

        update_payload = {field: new_value}
        response = requests.patch(Urls.USER, json=update_payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True

        if field in ("name", "email"):
            assert response.json()["user"][field] == new_value

    @allure.title('Изменение данных без авторизации — ошибка 401')
    def test_update_user_without_auth_fails(self):
        update_payload = {"name": "Updated_Name"}
        response = requests.patch(Urls.USER, json=update_payload, headers=Headers.JSON_HEADERS)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"