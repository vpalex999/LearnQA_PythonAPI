"""
Ex8
"""
import time
import requests


api_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# case 1
response1 = requests.get(api_url)
d_context1 = response1.json()
print(response1.text)

# case 2
response2 = requests.get(api_url, params={"token": response1.json()['token']})
assert response2.json()['status'] == "Job is NOT ready"

# case 3
time.sleep(response1.json()['seconds'])

# case 4
response3 = requests.get(api_url, params={'token': response1.json()['token']})
assert response3.json()['result'], "The field 'result' is not avaible"
assert response3.json()['status'] == "Job is ready"

