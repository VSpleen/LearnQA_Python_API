from requests import Response
import json
class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Получен ответ не в формате json. Полученный ответ - {response.text}"
        assert name in response_as_dict, f"В ответе отсутствует ключ {name}"
        assert response_as_dict[name]==expected_value, error_message
