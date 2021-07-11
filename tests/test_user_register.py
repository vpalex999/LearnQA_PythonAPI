import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):

        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):

        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    case_fill_data = [
        ({"email": "fake-local.com"}, (400, "Invalid email format")),
        ({"username": "a"}, (400, "The value of 'username' field is too short")),
        ({"username": "a"*251}, (400, "The value of 'username' field is too long")),
        ({"username": "a"*252}, (400, "The value of 'username' field is too long")),
    ]

    @pytest.mark.parametrize("case_field_value, expected",
                             case_fill_data,
                             ids=[text[1][1] for text in case_fill_data])
    def test_create_user_validation_field(self, case_field_value, expected):

        expected_status_code, expected_text = expected

        data = self.prepare_registration_data()
        data.update(case_field_value)

        response = MyRequests.post("/user/", data)

        Assertions.assert_code_status(response, expected_status_code)
        Assertions.assert_has_text_in(response, expected_text)

    case_fields_data = [
        ("email", 400),
        ("password", 400),
        ("username", 400),
        ("firstName", 400),
        ("lastName", 400),
    ]

    @pytest.mark.parametrize("name_field, expected_status_code",
                             case_fields_data,
                             ids=[field[0] for field in case_fields_data])
    def test_create_user_without_any_field(self, name_field,
                                           expected_status_code):
        data = self.prepare_registration_data()
        del data[name_field]

        response = MyRequests.put('/user/', data=data)

        Assertions.assert_code_status(response, expected_status_code)
        Assertions.assert_has_text_in(response, 'Auth token not supplied')
