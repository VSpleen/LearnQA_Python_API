from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):
    def test_delete_second_user(self):
        auth_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("user/login", data=auth_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        cookies = {"auth_sid": auth_sid}
        token = self.get_header(response1, "x-csrf-token")
        headers = {"x-csrf-token": token}

        response2 = MyRequests.delete("user/2", headers=headers, cookies=cookies)
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_content_value_utf_8(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        response3 = MyRequests.get("user/2", headers=headers, cookies=cookies)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(response3, "id", '2', "Пользователь был удален")

    def test_delete_user_successfully(self):
        # registration
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        cookies = {"auth_sid": auth_sid}
        token = self.get_header(response2, "x-csrf-token")
        headers = {"x-csrf-token": token}

        #delete
        response3 = MyRequests.delete(f"user/{user_id}", headers=headers, cookies=cookies)
        Assertions.assert_code_status(response3, 200)

        #check deleting
        response4 = MyRequests.get(f"user/{user_id}")
        Assertions.assert_code_status(response4, 404)
        Assertions.assert_content_value_utf_8(response4, 'User not found')


    def test_delete_another_user(self):
        # registration
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")


        register_data_another_user = self.prepare_registration_data()
        response2 = MyRequests.post("user/", data=register_data_another_user)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        username_another_user = register_data_another_user["username"]
        user_id_another = self.get_json_value(response2, "id")


        # login
        login_data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        cookies = {"auth_sid": auth_sid}
        token = self.get_header(response3, "x-csrf-token")
        headers = {"x-csrf-token": token}

        #delete
        response4 = MyRequests.delete(f"user/{user_id_another}", headers=headers, cookies=cookies)
        Assertions.assert_code_status(response4, 200)

        #check deleting
        response5 = MyRequests.get(f"user/{user_id}")
        Assertions.assert_code_status(response5, 404)
        Assertions.assert_content_value_utf_8(response5, 'User not found')

        response6 = MyRequests.get(f"user/{user_id_another}")
        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_value_by_name(response6, "username", f'{username_another_user}', "Пользователь был удален")
