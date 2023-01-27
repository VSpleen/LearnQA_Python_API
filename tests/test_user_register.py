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


    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_value(response, "id")


    def test_crate_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password':'123',
            'username':'learnqa',
            'firstName':'learnqa',
            'lastName':'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, f"Users with email '{email}' already exists")


    def test_create_user_with_incorect_email(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotovexample.com'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "Invalid email format")




    def test_create_user_with_too_short_name(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'q',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "The value of 'firstName' field is too short")


    def test_create_user_with_too_long_name(self):
        longName = "qwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfqhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkfsdfhghfdgkdfsgjdfhhgkdfghfdjdsqwqweqweqweqweqweqweqweqweqweqweqweqwfkf"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': longName,
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, "The value of 'firstName' field is too long")

    @pytest.mark.parametrize("dataset", exclude_data_list)
    def test_create_user_without_one_field(self, dataset):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=dataset["data"])
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_value_utf_8(response, f"The following required params are missed: {dataset['miss']}")
