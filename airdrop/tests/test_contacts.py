import unittest

from secure_drop import constants, exceptions
from secure_drop.singletons.ContactManager import ContactManager
from tests import test_constants, test_utils


class TestContactManagement(unittest.TestCase):
    def setUp(self):
        # Initialize a contact manager that all test cases can access
        self.contact_manager = ContactManager()

        # Ensure the contacts file does not exist before each test
        test_utils.safe_delete_file(constants.CONTACTS_FILE_PATH)

    def tearDown(self):
        # Delete the login manager instance so the next test receives a fresh one
        self.contact_manager.clear()

        # Clean up the contacts file after each test
        test_utils.safe_delete_file(constants.CONTACTS_FILE_PATH)

    def test_add_contact(self):
        """Test adding a contact."""

        # Ensure that the test contact is not yet in the contact list
        initial_contacts = self.contact_manager.get_contacts()
        contact_to_add = test_constants.TEST_CONTACT
        self.assertFalse(initial_contacts.contains(contact_to_add))

        # Add the test contact to the list
        self.contact_manager.add_contact(contact_to_add)

        # Ensure that the test contact is now in the list
        final_contatcs = self.contact_manager.get_contacts()
        self.assertTrue(final_contatcs.contains(contact_to_add))

    def test_duplicate_contact(self):
        """Test adding a duplicate contact."""

        # Ensure that the test contact is not yet in the contact list
        initial_contacts = self.contact_manager.get_contacts()
        contact_to_add = test_constants.TEST_CONTACT
        self.assertFalse(initial_contacts.contains(contact_to_add))

        # Add the test contact to the list
        self.contact_manager.add_contact(contact_to_add)

        # Attempt to add the same contact to the list
        with self.assertRaises(exceptions.ContactAlreadyAddedException):
            self.contact_manager.add_contact(contact_to_add)


if __name__ == '__main__':
    unittest.main()
