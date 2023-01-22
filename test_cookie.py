import requests
class TestCookie:
    def test_cookies(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(f"Полученная кука - {response.cookies}")
        assert response.status_code == 200, "Получен http код отличный от 200"
        assert "HomeWork" in response.cookies, "Ожидаемая кука отсутствует"
        assert "hw_value" == response.cookies.get("HomeWork"), "Значение куки отличается от ожидаемого"

