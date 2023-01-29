import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserEdit(BaseCase):
    def setup(self):
        # registration
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.firstName = register_data["firstName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response1, "id")

        # login
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.cookies = {"auth_sid": self.auth_sid}
        self.token = self.get_header(response2, "x-csrf-token")
        self.headers = {"x-csrf-token": self.token}


    def test_edit_user_successfully(self):
        #edit
        new_name = "Changed name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 data = {"firstName": new_name},
                                 headers = self.headers,
                                 cookies = self.cookies)
        Assertions.assert_code_status(response3, 200)

        #get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers=self.headers,
                                 cookies=self.cookies)
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Измененное имя отличается от ожидаемого")


    def test_edit_user_without_auth(self):
        # edit
        new_name = "Changed name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 400)
        # get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers=self.headers,
                                 cookies=self.cookies)
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", self.firstName,
                                             "Имя отличается от изначально созданного")



    def test_edit_user_by_another_user(self):
        #create another user
        register_data_for_second_user = self.prepare_registration_data()
        response3 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_for_second_user)

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        another_user_id = self.get_json_value(response3, "id")
        another_first_namme = register_data_for_second_user["firstName"]
        another_password = register_data_for_second_user["password"]
        another_email = register_data_for_second_user["email"]

        #try to change another user
        new_name = "Changed name"
        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{another_user_id}",
                                 data = {"firstName": new_name},
                                 headers = self.headers,
                                 cookies = self.cookies)
        Assertions.assert_code_status(response3, 200)

        #check current user's data
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers=self.headers,
                                 cookies=self.cookies)
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Измененное имя отличается от ожидаемого")

        #check another user's data
        login_data_another_user = {
            'email': another_email,
            'password': another_password
        }
        response5 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data_another_user)
        another_auth_sid = self.get_cookie(response5, "auth_sid")
        another_cookies = {"auth_sid": another_auth_sid}
        another_token = self.get_header(response5, "x-csrf-token")
        another_headers = {"x-csrf-token": another_token}
        response6 = requests.get(f"https://playground.learnqa.ru/api/user/{another_user_id}",
                                 headers=another_headers,
                                 cookies=another_cookies)
        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_value_by_name(response6, "firstName", another_first_namme,
                                             "Измененное имя отличается от ожидаемого")


    def test_edit_user_incorrect_email(self):
        #edit
        new_email = "someNamesomeDomain.com"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 data = {"email": new_email},
                                 headers = self.headers,
                                 cookies = self.cookies)
        Assertions.assert_code_status(response3, 400)

        #get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers=self.headers,
                                 cookies=self.cookies)
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "email", self.email, "Измененное имя отличается от ожидаемого")


    def test_edit_user_too_short_name(self):
        #edit
        new_name = "C"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 data = {"firstName": new_name},
                                 headers = self.headers,
                                 cookies = self.cookies)
        Assertions.assert_code_status(response3, 400)

        #get
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers=self.headers,
                                 cookies=self.cookies)
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", self.firstName, "Измененное имя отличается от ожидаемого")