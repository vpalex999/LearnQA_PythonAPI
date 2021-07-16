import json
import random
from datetime import datetime
from typing import Tuple

import allure
from requests import Response

from lib.my_requests import MyRequests


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        with allure.step(f"Get cookie '{cookie_name}' from response"):
            assert cookie_name in response.cookies, f"Cannot find cookie  with name {cookie_name} in the last response"
            return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        with allure.step(f"Get header '{headers_name}' from response"):
            assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
            return response.headers[headers_name]

    @staticmethod
    def get_json(response: Response):
        with allure.step("Get json from response"):
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                assert False, f"Response is not in JSON format. Response text is '{response.text}'"

    @staticmethod
    def get_json_value(response: Response, name):
        with allure.step(f"Get value from json by key '{name}'"):
            response_as_dict = BaseCase.get_json(response)

            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
            return response_as_dict[name]

    @allure.step
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = f'{datetime.now().strftime("%m%d%Y%H%M%S")}-{random.randint(100, 10000)}'
            email = f"{base_part}{random_part}@{domain}"

        _data = {
            'password': "123",
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        with allure.step(f"Prepared data: {_data}"):
            return _data

    @allure.step("Create new user")
    def create_user_gen(self) -> Tuple[Response, dict]:
        data = self.prepare_registration_data()
        return MyRequests.post('/user/', data=data), data

    @allure.step("Get 'auth_sid' from login response")
    def get_auth_sid(self, response: Response) -> str:
        return self.get_cookie(response, "auth_sid")

    @allure.step("Get 'x-csrf-token' from login response")
    def get_x_csrf_token(self, response: Response) -> str:
        return self.get_header(response, 'x-csrf-token')

    @allure.step("Get 'user_id' from login response")
    def get_auth_user_id(self, response: Response) -> str:
        return self.get_json_value(response, 'user_id')

    @allure.step("Get 'id' from response")
    def get_user_id(self, response: Response) -> str:
        return self.get_json_value(response, 'id')
