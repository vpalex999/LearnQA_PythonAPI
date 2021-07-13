import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password,
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, "x-csrf-token")

        # EDIT

        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name})

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit")

    def test_edit_user_without_auth(self):

        # CREATE USER
        response_create_user, *_ = self.create_user_gen()
        Assertions.assert_code_status(response_create_user, 200)

        # TRY MODIFY USER
        user_id = self.get_json_value(response_create_user, 'id')

        response_modify_user = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": "newFirstName"})

        Assertions.assert_code_status(response_modify_user, 400)
        Assertions.assert_has_text_in(
            response_modify_user, "Auth token not supplied")

    def test_edit_user_with_auth_other_user(self):
        # GREATE USERS
        response_create_user1, data_create_user1 = self.create_user_gen()
        Assertions.assert_code_status(response_create_user1, 200)

        response_create_user2, data_create_user2 = self.create_user_gen()
        Assertions.assert_code_status(response_create_user2, 200)

        # LOGIN USERs
        login_data_user1 = {
            'email': data_create_user1['email'],
            'password': data_create_user1['password'],
        }
        response_login_user1 = MyRequests.post(
            "/user/login/", data=login_data_user1)

        Assertions.assert_code_status(response_login_user1, 200)

        login_data_user2 = {
            "email": data_create_user2['email'],
            'password': data_create_user2['password'],
        }

        response_login_user2 = MyRequests.post(
            "/user/login/", data=login_data_user2)

        # TRY MODIFY USER2 WITH AUTH OF USER1
        user_id_user2 = self.get_json_value(response_create_user2, 'id')
        token_user1 = self.get_header(response_login_user1, "x-csrf-token")
        auth_sid_user1 = self.get_cookie(response_login_user1, "auth_sid")

        response_modify_user2 = MyRequests.put(
            f"/user/{user_id_user2}",
            headers={'x-csrf-token': token_user1},
            cookies={"auth_sid": auth_sid_user1},
            data={'firstName': "newName"})
        Assertions.assert_code_status(response_modify_user2, 200)

        token_user2 = self.get_header(response_login_user2, "x-csrf-token")
        auth_sid_user2 = self.get_cookie(response_login_user2, "auth_sid")

        # CHECK MODIFIED DATA FROM USER2

        response_get_data_user2 = MyRequests.get(
            f"/user/{user_id_user2}",
            headers={'x-csrf-token': token_user2},
            cookies={"auth_sid": auth_sid_user2})

        expected_value_user2 = data_create_user2["firstName"]
        actual_value_user2 = self.get_json_value(
            response_get_data_user2, "firstName")

        Assertions.assert_json_value_by_name(
            response_get_data_user2,
            "firstName",
            expected_value_user2,
            f"Unexpected value of attribute 'firstName'. Expected: {expected_value_user2}, Actual: {actual_value_user2}")

    case_wrong_data = [
        ({'email': "wrongdot.com"}, (400, "Invalid email format")),
        ({'firstName': "a"}, (400, "The value of 'firstName' field is too short"))
    ]

    @pytest.mark.parametrize("input_data, expected", case_wrong_data)
    def test_modify_user_with_wrong_data(self, input_data, expected):
        # GREATE USER
        response_create_user1, data_create_user1 = self.create_user_gen()
        Assertions.assert_code_status(response_create_user1, 200)

        # LOGIN USER
        login_data_user1 = {
            'email': data_create_user1['email'],
            'password': data_create_user1['password'],
        }
        response_login_user1 = MyRequests.post(
            "/user/login/", data=login_data_user1)

        Assertions.assert_login_user(response_login_user1)

        user_id = self.get_json_value(response_create_user1, 'id')
        token = self.get_header(response_login_user1, 'x-csrf-token')
        auth_sid = self.get_cookie(response_login_user1, "auth_sid")

        # TRY MODIFY USER
        response_modify_user = MyRequests.put(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={"auth_sid": auth_sid},
            data=input_data)

        expected_status_code, expected_text = expected

        Assertions.assert_code_status(response_modify_user, expected_status_code)
        Assertions.assert_has_text_in(response_modify_user, expected_text)
