import pytest
import requests


class TestCookie:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        homework_cookie = response.cookies.get('HomeWork')
        expected_cookie_value = 'hw_value'
        assert homework_cookie == expected_cookie_value, f"Wrong HomeWork cookie value. Should be {expected_cookie_value}"
