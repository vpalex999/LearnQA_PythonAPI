import allure
from requests import Response

from lib.base_case import BaseCase


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        with allure.step(f"Assert json key '{name}' has expected value '{expected_value}'"):
            response_value = BaseCase.get_json_value(response, name)
            assert response_value == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        with allure.step(f"Assert response json has key '{name}'"):
            assert BaseCase.get_json_value(response, name)

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        with allure.step(f"Assert response json has not the key '{name}'"):
            response_as_dict = BaseCase.get_json(response)
            assert name not in response_as_dict, \
                f"Response JSON has key '{name}' in {response_as_dict} but shouldn't has it"

    @staticmethod
    def assert_json_has_keys(response: Response, keys_name):
        with allure.step(f"Assert response json has keys '{keys_name}'"):
            for name in keys_name:
                assert BaseCase.get_json_value(response, name)

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        with allure.step(f"Assert response has status code '{expected_status_code}'"):
            assert response.status_code == expected_status_code, \
                (f"Unexpected status code! Expected:{expected_status_code}. "
                 f"Actual:{response.status_code}")

    @staticmethod
    def assert_has_text_in(response: Response, expected_text: str):
        with allure.step(f"Assert response has text '{expected_text}'"):
            assert expected_text in response.text, \
                (f"Unexpected text! Expected: {expected_text}. "
                 f"Actual: {response.text}")

    @ staticmethod
    def assert_login_user(response: Response):
        with allure.step("Assert login user"):
            user_id = BaseCase.get_json_value(response, "user_id")
            assert user_id != 0, f"User whith id '{user_id}' is not authorize."

    @ staticmethod
    def assert_create_user(response: Response):
        with allure.step("Assert user successful create"):
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, 'id')

    @ staticmethod
    def assert_user_not_found(response: Response):
        with allure.step("Assert response user not found"):
            Assertions.assert_code_status(response, 404)
            Assertions.assert_has_text_in(response, 'User not found')
