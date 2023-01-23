import json

import requests
import pytest
from json.decoder import JSONDecodeError

class TestUa:
    parameters = [
        ({'agent':'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'exp_values':{'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}}),
        ({'agent':'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1', 'exp_values':{'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}}),
        ({'agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'exp_values':{'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}}),
        ({'agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0', 'exp_values':{'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}}),
        ({'agent':'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1''Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', 'exp_values':{'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}})
    ]


    @pytest.mark.parametrize('prmtrs', parameters)
    def test_user_agent(self, prmtrs):
        ua = {"User-Agent":prmtrs["agent"]}
        response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=ua)
        print('\n\n')
        print(response.text)
        assert response.status_code == 200, f'Получен отличный от 200 статус кода http ответа'
        assert "device" in response.json(), f'В полученном json отсутствует поле device'
        try:
            assert response.json()['device']==prmtrs['exp_values']['device'], f'Полученное значение device отлиичается от ожидаемого'
        except json.JSONDecodeError:
            print('Не удалось распарсить json при обработке поля device')

        assert "browser" in response.json(), f'В полученном json отсутствует поле browser'
        try:
            assert response.json()['browser']==prmtrs['exp_values']['browser'], f'Полученное значение browser отлиичается от ожидаемого'
        except json.JSONDecodeError:
            print('Не удалось распарсить json при обработке поля browser')

        assert "platform" in response.json(), f'В полученном json отсутствует поле platform'
        try:
            assert response.json()['platform']==prmtrs['exp_values']['platform'], f'Полученное значение platform отлиичается от ожидаемого'
        except json.JSONDecodeError:
            print('Не удалось распарсить json при обработке поля platform')
