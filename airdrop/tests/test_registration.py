import unittest

from secure_drop import constants, utils
from secure_drop.registration import register_user
from tests import test_constants, test_utils


class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        # Ensure the user file does not exist before each test
        test_utils.safe_delete_file(constants.USER_FILE_PATH)

    def tearDown(self):
        # Clean up the user file after each test
        test_utils.safe_delete_file(constants.USER_FILE_PATH)

    def test_successful_registration(self):
        """Test successful user registration."""  

        self.assertFalse(utils.user_registered())
        register_user(test_constants.TEST_CREDENTIALS)
        self.assertTrue(utils.user_registered())


if __name__ == '__main__':
    unittest.main()
