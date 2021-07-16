import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Delete cases")
class TestUserDelete(BaseCase):

    @allure.description("Trying to delete protected user should failed")
    def test_delete_protected_user(self):

        data = {
            'email': "vinkotov@example.com",
            'password': '1234',
        }

        with allure.step(f"Login user as id=2 with auth data: {data}"):

            response_login = MyRequests.post('/user/login/', data=data)
            Assertions.assert_login_user(response_login)

        with allure.step("Delete user id=2"):
            token = self.get_x_csrf_token(response_login)
            auth_sid = self.get_auth_sid(response_login)

            response_delete = MyRequests.delete(
                '/user/2',
                cookies={'auth_sid': auth_sid},
                headers={'x-csrf-token': token}
            )

            Assertions.assert_code_status(response_delete, 400)
            Assertions.assert_has_text_in(
                response_delete,
                'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'
            )

    def test_delete_user(self):
        """Trying to delete regular user"""

        with allure.step("Create test user"):
            response_create_user, data_create_user = self.create_user_gen()
            Assertions.assert_create_user(response_create_user)

        with allure.step("Login as created user"):
            data = {
                'email': data_create_user['email'],
                'password': data_create_user['password'],
            }

            response_login = MyRequests.post('/user/login/', data=data)
            Assertions.assert_login_user(response_login)

        with allure.step("Delete authorized user"):
            token = self.get_x_csrf_token(response_login)
            auth_sid = self.get_auth_sid(response_login)
            user_id = self.get_auth_user_id(response_login)

            response_delete = MyRequests.delete(
                f'/user/{user_id}',
                cookies={'auth_sid': auth_sid},
                headers={'x-csrf-token': token}
            )

            Assertions.assert_code_status(response_delete, 200)

        with allure.step("Check user was deleted"):
            response_get_user_info = MyRequests.get(f"/user/{user_id}")
            Assertions.assert_user_not_found(response_get_user_info)

    def test_delere_user_from_other_auth_user_data(self):
        """Delete user with using autentication data from other logged user."""

        with allure.step("Create test users"):
            response_create_user1, data_create_user1 = self.create_user_gen()
            Assertions.assert_create_user(response_create_user1)

            response_create_user2, data_create_user2 = self.create_user_gen()
            Assertions.assert_create_user(response_create_user2)

        with allure.step("Login as user1"):
            data_login_user1 = {
                'email': data_create_user1['email'],
                'password': data_create_user1['password'],
            }

            response_login_user1 = MyRequests.post(
                '/user/login/', data=data_login_user1)
            Assertions.assert_login_user(response_login_user1)

        with allure.step("Delete user 2"):
            with allure.step("Get auth data from user1"):
                token_user1 = self.get_x_csrf_token(response_login_user1)
                auth_sid_user1 = self.get_auth_sid(response_login_user1)

            user_id_user2 = self.get_user_id(response_create_user2)

            response_delete = MyRequests.delete(
                f'/user/{user_id_user2}',
                cookies={'auth_sid': auth_sid_user1},
                headers={'x-csrf-token': token_user1}
            )

            Assertions.assert_code_status(response_delete, 400)
