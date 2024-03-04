import pytest
import requests

class TestHeader:
    def test_homework_header(self):
        url = 'https://playground.learnqa.ru/api/homework_header'
        response = requests.get(url)
        secret_header = 'x-secret-homework-header'
        x_secret_homework_header = response.headers.get(secret_header)
        expected_value = 'Some secret value'

        assert secret_header in response.headers, f"There is no secret header '{secret_header}' in the response."
        assert x_secret_homework_header == expected_value, f"Wrong '{x_secret_homework_header}' value."
