import unittest

from secure_drop import constants
from secure_drop.registration import register_user
from secure_drop.singletons.LoginManager import LoginManager
from tests import test_constants, test_utils


class TestUserLogin(unittest.TestCase):
    def setUp(self):
        # Initialize a login manager that all test cases can access
        self.login_manager = LoginManager()

        # Register a new user
        test_utils.safe_delete_file(constants.USER_FILE_PATH)
        register_user(test_constants.TEST_CREDENTIALS)

    def tearDown(self):
        # Delete the login manager instance so the next test receives a fresh one
        self.login_manager.clear()

        # Delete the registered user
        test_utils.safe_delete_file(constants.USER_FILE_PATH)

    def test_successful_login(self):
        """Test successful user login."""

        self.login_manager.login_user(test_constants.TEST_CREDENTIALS.email, test_constants.TEST_CREDENTIALS.password)
        self.assertTrue(self.login_manager.logged_in())

    def test_invalid_email_login(self):
        """Test login with invalid email."""

        self.login_manager.login_user(test_constants.TEST_CREDENTIALS.email + "blah", test_constants.TEST_CREDENTIALS.password)
        self.assertFalse(self.login_manager.logged_in())

    def test_invalid_password_login(self):
        """Test login with incorrect password."""

        self.login_manager.login_user(test_constants.TEST_CREDENTIALS.email, test_constants.TEST_CREDENTIALS.password + "blah")
        self.assertFalse(self.login_manager.logged_in())

    def test_invalid_email_and_password(self):
        """Test login with incorrect email and password."""

        self.login_manager.login_user(test_constants.TEST_CREDENTIALS.email + "blah", test_constants.TEST_CREDENTIALS.password + "blah")
        self.assertFalse(self.login_manager.logged_in())

    def test_max_login_attempts(self):
        """Test exceeding maximum login attempts."""

        bad_email = "blah"
        bad_password = "blah"
        for _ in range(constants.MAX_LOGIN_ATTEMPTS):
            self.login_manager.login_user(bad_email, bad_password)

        self.assertTrue(self.login_manager.max_login_attempts_exceeded())


if __name__ == '__main__':
    unittest.main()
