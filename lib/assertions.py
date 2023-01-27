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

    @staticmethod
    def assert_json_has_value (response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Получен ответ не в формате json. Полученный ответ - {response.text}"
        assert name in response_as_dict, f"В ответе отсутствует ключ {name}"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Полученный код http ответа отличается" \
                                                            f" от ожидаемого получен код - {response.status_code}," \
                                                            f" а ожидался {expected_status_code}"

    @staticmethod
    def assert_content_value_utf_8 (response: Response, expected_contetnt):
        assert response.content.decode("utf-8") == expected_contetnt, \
            f"Полученный контент отличается от ожидаемого, получено {response.content.decode('utf-8')}" \
            f"Ожидалось {expected_contetnt}"