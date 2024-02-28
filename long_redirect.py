import requests

url = "https://playground.learnqa.ru/api/long_redirect"

response = requests.get(url)

redirects_count = len(response.history)

print(f"Redirects count: {redirects_count}")
print(f"Final url: {response.url}")