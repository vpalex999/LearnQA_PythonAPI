import requests
import allure

from lib.logger import Logger
from environment import ENV_OBJECT


class MyRequests:

    @staticmethod
    def get(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "GET")

    @staticmethod
    def post(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "POST")

    @staticmethod
    def put(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "PUT")

    @staticmethod
    def delete(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(uri: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{ENV_OBJECT.get_base_url()}{uri}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == "GET":
            response = requests.get(
                url, params=data, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(
                url, data=data, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(
                url, data=data, headers=headers, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(
                url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)
        return response
