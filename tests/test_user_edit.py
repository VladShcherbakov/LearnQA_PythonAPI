import pytest
import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserEdit(BaseCase):
    wrong_email_cases = [
        ("email_without_@"),
        ("one_char_email")
    ]

    def test_edit_just_created_user(self):
        user = self._prepare_user()

        email = user['email']
        first_name = user['firstName']
        password = user['password']
        user_id = user["id"]

        #Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Change name"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_data_when_not_auth(self):
        user = self._prepare_user()

        user_id = user['id']
        new_name = 'Changed name'

        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": ''},
            cookies={"auth_sid": ''},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        expected_error_text = 'Auth token not supplied'
        assert response.text == 'Auth token not supplied', f"Response should have '{expected_error_text}' error"

    def test_edit_user_data_auth_another_user(self):
        user = self._prepare_user()
        user2 = self._prepare_user()

        user_id = user["id"]
        user_first_name = user['firstName']

        user2_email = user2['email']
        user2_password = user2['password']

        # Login
        login_data = {
            'email': user2_email,
            'password': user2_password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Change name"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)


        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_has_not_key(response4, "firstName")

        Assertions.assert_json_value_by_name(
            response4,
            "username",
            user_first_name,
            "Wrong name of the user after edit"
        )

    @pytest.mark.parametrize("case", wrong_email_cases)
    def test_edit_user_data_wrong_email(self, case):
        user = self._prepare_user()

        email = user['email']
        first_name = user['firstName']
        password = user['password']
        user_id = user["id"]

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        if case == "email_without_@":
            #remove @ from the new email
            new_email = email.replace('@', '')
        elif case == "one_char_email":
            #get only one char of email
            new_email = email[0]
        else:
            raise Exception(f"Unknown wrong email test case '{case}'!")

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        expected_error = 'Invalid email format'
        assert response3.text == expected_error, f"Response should have '{expected_error}' error"

    def _prepare_user(self):
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        return {
            "email": register_data['email'],
            "firstName": register_data['firstName'],
            "password": register_data['password'],
            "id": self.get_json_value(response1, "id")
        }
