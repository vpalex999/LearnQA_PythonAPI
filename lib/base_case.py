import json
import random
from datetime import datetime
from typing import Tuple

from requests import Response

from lib.my_requests import MyRequests


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie  with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    @staticmethod
    def get_json(response: Response):
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

    @staticmethod
    def get_json_value(response: Response, name):
        response_as_dict = BaseCase.get_json(response)

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = f'{datetime.now().strftime("%m%d%Y%H%M%S")}-{random.randint(100, 10000)}'
            email = f"{base_part}{random_part}@{domain}"

        return {
            'password': "123",
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def create_user_gen(self) -> Tuple[Response, dict]:
        data = self.prepare_registration_data()
        return MyRequests.post('/user/', data=data), data
