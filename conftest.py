import allure
import pytest
import requests

from data import Urls, Headers
from helpers import generate_random_user


@pytest.fixture(scope="function")
def create_user():
    payload = generate_random_user()
    with allure.step("Создать тестового пользователя через API"):
        response = requests.post(Urls.REGISTER, json=payload, headers=Headers.JSON_HEADERS)

    token = None
    if response.status_code == 200:
        token = response.json().get("accessToken")

    user_data = {
        "payload": payload,
        "token": token,
        "response": response
    }

    yield user_data

    if token:
        delete_headers = {
            "Authorization": token,
            **Headers.JSON_HEADERS
        }
        with allure.step("Удалить тестового пользователя через API"):
            requests.delete(Urls.USER, headers=delete_headers)