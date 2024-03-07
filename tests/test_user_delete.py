import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_undeletable_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': 1234
        }

        response = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response, "user_id")

        response2 = MyRequests.get(
            "user/auth",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

        response3 = MyRequests.delete(
            f"user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "User with ID 1, 2, 3, 4 or 5 must be undeletable!"
        )

    def test_delete_user_with_auth(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response2 = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

        response3 = MyRequests.delete(
            f"user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"user/{user_id_from_auth_method}")

        assert response4.text == 'User not found', \
            f"Wrong response text '{response4.text}'. User '{user_id_from_auth_method}' should be deleted"

    def test_delete_user_auth_another_user(self):
        user = self._prepare_user()
        user2 = self._prepare_user()

        user_id = user["id"]

        user2_email = user2['email']
        user2_password = user2['password']

        # Login
        login_data = {
            'email': user2_email,
            'password': user2_password
        }

        response = MyRequests.post("user/login", data=login_data)

        user2_auth_sid = self.get_cookie(response, "auth_sid")
        user2_token = self.get_header(response, "x-csrf-token")

        response2 = MyRequests.delete(
            f"user/{user_id}",
            headers={"x-csrf-token": user2_token},
            cookies={"auth_sid": user2_auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "This user can only delete their own account.",
            "User should not be deleted if auth with another user"
        )

    def _prepare_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        return {
            "email": register_data['email'],
            "firstName": register_data['firstName'],
            "password": register_data['password'],
            "id": self.get_json_value(response1, "id")
        }
