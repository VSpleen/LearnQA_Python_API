import json.decoder
from requests import Response
from datetime import datetime

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Кука с именем {cookie_name} не найдена в ответе"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Хедер с именем {header_name} не найдена в ответе"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Получен ответ не в формате json. Полученный ответ - {response.text}"
        assert name in response_as_dict, f"В ответе отсутствует ключ {name}"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email==None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }