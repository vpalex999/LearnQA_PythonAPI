from requests import Response

from lib.base_case import BaseCase


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        response_value = BaseCase.get_json_value(response, name)
        assert response_value == expected_value, error_message
