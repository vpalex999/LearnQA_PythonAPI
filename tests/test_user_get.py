import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Get cases")
class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_name(self):

        with allure.step("Login as known user"):
            data = {
                'email': "vinkotov@example.com",
                'password': '1234',
            }

            response1 = MyRequests.post("/user/login", data=data)

        with allure.step("Get user info"):
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, 'x-csrf-token')
            user_id_from_auth_method = self.get_json_value(
                response1, 'user_id')

            response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                       headers={'x-csrf-token': token},
                                       cookies={"auth_sid": auth_sid})

        with allure.step("Check data has fields exactly"):
            Assertions.assert_json_has_keys(
                response2, ("username", "email", "firstName", "lastName"))

    def test_get_user_data_with_auth_other_user_id(self):

        with allure.step("Create test users"):
            data_reg_user1 = self.prepare_registration_data()

            response_create_user1 = MyRequests.post(
                '/user/', data=data_reg_user1)
            Assertions.assert_code_status(response_create_user1, 200)

            data_reg_user2 = self.prepare_registration_data()
            response_create_user2 = MyRequests.post(
                '/user/', data=data_reg_user2)
            Assertions.assert_code_status(response_create_user2, 200)

        with allure.step("Login users"):
            response_login_user1 = MyRequests.post("/user/login/",
                                                   data={
                                                       "email": data_reg_user1["email"],
                                                       "password": data_reg_user1["password"]
                                                   })

            response_login_user2 = MyRequests.post("/user/login/",
                                                   data={
                                                       "email": data_reg_user2["email"],
                                                       "password": data_reg_user2["password"]
                                                   })

        with allure.step("Try get data of user2 using auth data of user1"):
            auth_sid_user1 = self.get_cookie(response_login_user1, "auth_sid")

            token_user2 = self.get_header(response_login_user2, "x-csrf-token")
            user_id_user2 = self.get_json_value(response_login_user2, "user_id")

            response_get_data_user2 = MyRequests.get(f"/user/{user_id_user2}",
                                                     headers={
                                                         "x-csrf-token": token_user2},
                                                     cookies={"auth_sid": auth_sid_user1})

        Assertions.assert_json_has_key(response_get_data_user2, "username")
        Assertions.assert_json_has_not_key(response_get_data_user2, "email")
        Assertions.assert_json_has_not_key(
            response_get_data_user2, "firstName")
        Assertions.assert_json_has_not_key(response_get_data_user2, "lastName")
