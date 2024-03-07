import pytest
import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("user/2")

        Assertions.assert_json_has_key(response, "username")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response = MyRequests.post('user/login', data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response, "user_id")

        response2 = MyRequests.get(
            f"user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_by_another_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response, "user_id")
        another_user_id = '1'

        assert user_id_from_auth_method != another_user_id, f"Different user ids are the same but should not!"

        response2 = MyRequests.get(
            f"user/{another_user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        not_expected_keys = ['email', 'firstName', 'lastName']
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, not_expected_keys)
