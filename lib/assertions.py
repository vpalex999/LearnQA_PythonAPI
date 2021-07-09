from requests import Response

from lib.base_case import BaseCase


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        response_value = BaseCase.get_json_value(response, name)
        assert response_value == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        assert BaseCase.get_json_value(response, name)

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        response_as_dict = BaseCase.get_json(response)
        assert name not in response_as_dict, f"Response JSON has key '{name}' in {response_as_dict} but shouldn't has it"

    @staticmethod
    def assert_json_has_keys(response: Response, names):
        for name in names:
            assert BaseCase.get_json_value(response, name)

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected:{expected_status_code}. Actual:{response.status_code}"
