"""
Ex7
"""
import requests


api_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

print("--- case 1. ---")
response = requests.get(api_url)
print("The response is:", response.text)

print("--- case 2. ---")
response = requests.post(api_url, data={'method': "HEAD"})
print("The response is:", response.text)

print("--- case 3. ---")
response = requests.put(api_url, data={'method': "PUT"})
print("The response is:", response.text)

print("--- case 4. ---")
methods_name = {"GET": lambda rq, url, data: rq.get(url, params=data),
                "POST": lambda rq, url, data: rq.post(url, data=data),
                "PUT": lambda rq, url, data: rq.put(url, data=data),
                "DELETE": lambda rq, url, data: rq.delete(url, data=data)}

for req_name, req_method in methods_name.items():
    for send_method in methods_name:
        response = req_method(requests, api_url, {'method': send_method})

        print(f"req_method: {req_name}, data: {send_method}, response text: {response.text}, status: {response.status_code}")

        if req_name != send_method and '{"success":"!"}' in response.text:
            print(f"Wrong case: request method={req_name}, data={send_method}, answer='{response.text}' ")
