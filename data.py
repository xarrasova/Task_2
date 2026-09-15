class Urls:
    MAIN_URL = 'https://stellarburgers.education-services.ru'
    REGISTER = f'{MAIN_URL}/api/auth/register'
    LOGIN = f'{MAIN_URL}/api/auth/login'
    USER = f'{MAIN_URL}/api/auth/user'
    ORDERS = f'{MAIN_URL}/api/orders'


class Headers:
    JSON_HEADERS = {"Content-Type": "application/json"}