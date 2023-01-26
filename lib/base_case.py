import json.decoder
from requests import Response

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
