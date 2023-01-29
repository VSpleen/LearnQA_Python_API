import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Кейсы регистрации пользователя")
class TestUserRegister(BaseCase):
    exclude_data_list = [
        ({"miss":"password", "data" : {'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': "learnqa@example.com"}}),
        ({"miss": "username", "data": {'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa','email': "learnqa@example.com"}}),
        ({"miss": "firstName", "data": {'password': '123', 'username': 'learnqa', 'lastName': 'learnqa','email': "learnqa@example.com"}}),
        ({"miss": "lastName", "data": {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa','email': "learnqa@example.com"}}),
        ({"miss": "email", "data": {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa',}}),
    ]


    @allure.description("Кейс успешной регистрации пользователя")
    def test_create_user_successfully(self):
        response = MyRequests.post("user/", data=self.prepare_registration_data())
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    @allure.description("Кейс регистации пользователя с занятым имейлом")
    def test_crate_user_with_existing_email(self):
        response = MyRequests.post("user/", data=self.prepare_registration_data('vinkotov@example.com'))
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, f"Users with email 'vinkotov@example.com' already exists")


    @allure.description("Кейс регистрации пользователя с некорректным иммейлом")
    def test_create_user_with_incorect_email(self):
        response = MyRequests.post("user/", data=self.prepare_registration_data('vinkotovexample.com'))
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "Invalid email format")


    @allure.description("Кейс регистрации пользователя со слишком коротким именем")
    def test_create_user_with_too_short_name(self):
        data = self.prepare_registration_data()
        data['firstName']='q'
        response = MyRequests.post("user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "The value of 'firstName' field is too short")


    @allure.description("Кейс регистрации пользователя со слишком длинным именем")
    def test_create_user_with_too_long_name(self):
        longName = "qwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfqhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkf"
        data = self.prepare_registration_data()
        data['firstName'] = longName
        response = MyRequests.post("user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "The value of 'firstName' field is too long")


    @allure.description("Параметризированные кейсы с отстутствием обязательного параметра")
    @pytest.mark.parametrize("dataset", exclude_data_list)
    def test_create_user_without_one_field(self, dataset):
        response = MyRequests.post("user/", data=dataset["data"])
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, f"The following required params are missed: {dataset['miss']}")
