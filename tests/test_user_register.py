import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
class TestUserRegister(BaseCase):
    exclude_data_list = [
        ({"miss":"password", "data" : {'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': "learnqa@example.com"}}),
        ({"miss": "username", "data": {'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa','email': "learnqa@example.com"}}),
        ({"miss": "firstName", "data": {'password': '123', 'username': 'learnqa', 'lastName': 'learnqa','email': "learnqa@example.com"}}),
        ({"miss": "lastName", "data": {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa','email': "learnqa@example.com"}}),
        ({"miss": "email", "data": {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa',}}),
    ]



    def test_create_user_successfully(self):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.prepare_registration_data())
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    def test_crate_user_with_existing_email(self):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.prepare_registration_data('vinkotov@example.com'))
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, f"Users with email 'vinkotov@example.com' already exists")


    def test_create_user_with_incorect_email(self):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=self.prepare_registration_data('vinkotovexample.com'))
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "Invalid email format")




    def test_create_user_with_too_short_name(self):
        data = self.prepare_registration_data()
        data['firstName']='q'
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "The value of 'firstName' field is too short")


    def test_create_user_with_too_long_name(self):
        longName = "qwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfqhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkf"
        data = self.prepare_registration_data()
        data['firstName'] = longName
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "The value of 'firstName' field is too long")

    @pytest.mark.parametrize("dataset", exclude_data_list)
    def test_create_user_without_one_field(self, dataset):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=dataset["data"])
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, f"The following required params are missed: {dataset['miss']}")
