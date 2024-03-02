import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1. HTTP-request without method param
response = requests.get(url)
print(f"1. No 'method' param: {response.text}")

# 2. HEAD-request
response = requests.head(url)
print(f"2. HEAD request: {response.text}")

# 3. right GET request
reponse = requests.get(url, params={"method":"GET"})
print(f"3. GET request: {response.text}")

# 4. Check all methods and params
methods = ["GET", "POST", "PUT", "DELETE"]
for method in methods:
    for param_method in methods:
        if method == 'GET':
            response = requests.request(method=method, url=url, params={"method": param_method})
        else:
            response = requests.request(method=method, url=url, data={"method": param_method})
        print(f"Real method: {method}, param 'method': {param_method}, response: {response.text}")
