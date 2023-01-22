import requests
class TestHeader:
    def test_headers(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(f"Полученные хедеры - {response.headers}")
        assert response.status_code == 200, "Получен http код отличный от 200"
        assert "x-secret-homework-header" in response.headers, "Ожидаемый хедер отсутствует"
        assert "Some secret value" == response.headers.get("x-secret-homework-header"), f"Значение хедера x-secret-homework-header отличается от ожидаемого"

