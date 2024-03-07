import pytest
import requests
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    cases = [
        ("userwithoutatexample.com", "Invalid email format"),
        ("nousernamefield@example.com", "The following required params are missed: username"),
        ("u", "The value of 'email' field is too short"),
        ("verylonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong" +
         "longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong" +
         "longlonglonglonglonglonglonglonglongemail@example.com", "The value of 'email' field is too long"),
    ]

    @pytest.mark.parametrize("email, expected_error", cases)
    def test_create_user_with_existing_email(self, email, expected_error):
        data = {
            "username": 'learnqa',
            "firstName": 'learnqa',
            "lastName": 'learnqa',
            "email": email,
            "password": '1234'
        }

        if email == "nousernamefield@example.com":
            del data["username"]

        response = MyRequests.post("user", data=data)

        assert response.status_code == 400, f"Unexpected status code '{response.status_code}'"
        assert response.text == expected_error, f"Unexpected response content '{response.text}'"
