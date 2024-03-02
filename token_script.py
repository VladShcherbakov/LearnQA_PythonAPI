import json
import requests
import time

EXPECTED_RESULT = "42"
EXPECTED_JOB_STATUS = "Job is ready"

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(url)

response_data = json.loads(response.text)
token, seconds_to_wait = response_data['token'], response_data['seconds']

time.sleep(seconds_to_wait)

second_response = requests.get(url, params={"token": token})

second_response_data = json.loads(second_response.text)

assert second_response_data["result"] == EXPECTED_RESULT, "Wrong result!"
assert second_response_data["status"] == EXPECTED_JOB_STATUS, "Wrong job status!"
