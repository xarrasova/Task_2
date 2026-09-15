import random
import string

import allure
import requests

from data import Urls


def get_valid_ingredient_ids(count=2):
    with allure.step("Получить список ингредиентов через API"):
        response = requests.get(f'{Urls.MAIN_URL}/api/ingredients')

    assert response.status_code == 200, f"Не удалось получить ингредиенты: {response.text}"

    data = response.json()
    ingredients = data.get("data") or data.get("ingredients")

    assert ingredients, f"Список ингредиентов пуст или не найден. Ответ: {data}"

    return [item["_id"] for item in ingredients[:count]]


def generate_random_user():
    email = f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@yandex.ru"
    password = ''.join(random.choices(string.digits, k=8))
    name = f"User_{''.join(random.choices(string.ascii_uppercase, k=5))}"
    return {"email": email, "password": password, "name": name}