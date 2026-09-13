import pytest
import requests

from data import Urls, Headers
from helpers import generate_random_user


@pytest.fixture(scope="function")
def create_user():
    """Создание пользователя через API и его удаление после теста"""
    payload = generate_random_user()

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
        requests.delete(Urls.USER, headers=delete_headers)