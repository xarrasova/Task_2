import requests
from data import Urls
import random
import string

def get_valid_ingredient_ids(count=2):
    """
    Получает актуальные ID ингредиентов с сервера.
    Возвращает список из `count` ID.
    """
    response = requests.get(f'{Urls.MAIN_URL}/api/ingredients')
    assert response.status_code == 200, f"Не удалось получить ингредиенты: {response.text}"
    
    data = response.json()
    # Проверяем, где лежит список (может быть "data" или "ingredients")
    ingredients = data.get("data") or data.get("ingredients")
    
    assert ingredients, f"Список ингредиентов пуст или не найден. Ответ: {data}"
    
    return [item["_id"] for item in ingredients[:count]]

def generate_random_user():
    """Генерация уникального email и пароля"""
    email = f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@yandex.ru"
    password = ''.join(random.choices(string.digits, k=8))
    name = f"User_{''.join(random.choices(string.ascii_uppercase, k=5))}"
    return {"email": email, "password": password, "name": name}