import unittest
import filecmp
import os

from secure_drop.types.ContactList import ContactList
from secure_drop.types.Credentials import Credentials
from tests import test_constants
# from secure_drop.crypto import encrypt_AES, decrypt_AES


class TestCrypto(unittest.TestCase):
    def test_credentials_encryption(self):
        """Verifies that credentials can be encrypted, decrypted, and read from."""

        credentials = test_constants.TEST_CREDENTIALS
        encrypted_credentials = credentials.to_encrypted_json()
        decrypted_credentials = Credentials.from_encrypted_json(encrypted_credentials)
        self.assertEqual(credentials.email, decrypted_credentials.email)
        self.assertEqual(credentials.password, decrypted_credentials.password)
       
    def test_contact_list_encryption(self):
        """Verifies that contact lists can be encrypted, decrypted, and read from."""
 
        contact_list = ContactList()
        contact_list.add_contact(test_constants.TEST_CONTACT)
        encrypted_contact_list = contact_list.to_encrypted_json()
        decrypted_contact_list = ContactList.from_encrypted_json(encrypted_contact_list)
        for decrypted_contact in decrypted_contact_list:
            # Ensure that each contact in the decrypted contact list is present in the original contact list
            self.assertTrue(contact_list.contains(decrypted_contact))

    
    # TODO
    # def test_aes_encryption_decryption(self):
    #     """Test AES encryption and decryption of a large file for essentially testing speed."""

    #     original_file_path = 'test_file.txt'
    #     encrypted_file_path = 'test_file.txt.aes'
    #     decrypted_file_path = 'test_file_decrypted.txt'  # Changed decrypted file path

    #     # Create a test file
    #     with open(original_file_path, 'wb') as f:
    #         f.write(os.urandom(50 * 1024 * 1024))  # Creates a 50MB test file 

    #     # Encrypt the file
    #     encrypted_aes_key, encrypted_file = encrypt_AES(original_file_path)
        
    #     # Decrypt the file
    #     decrypt_AES(encrypted_file, encrypted_aes_key)  # The decrypted file is saved as 'test_file_decrypted.txt'

    #     # Compare original and decrypted files
    #     self.assertTrue(filecmp.cmp(original_file_path, decrypted_file_path),
    #                     "Decrypted file does not match the original.")

    #     # Cleanup
    #     os.remove(original_file_path)
    #     os.remove(encrypted_file)
    #     os.remove(decrypted_file_path)

    # def test_aes_encryption_decryption_with_image(self):
    #     """Test AES encryption and decryption of an image file."""

    #     original_file_path = 'tests\assets\test_picture.jpg'
    #     encrypted_file_path = original_file_path + '.aes'

    #     # Encrypt the file
    #     encrypted_aes_key, encrypted_file = encrypt_AES(original_file_path)
        
    #     # Decrypt the file
    #     decrypted_file_path = decrypt_AES(encrypted_file, encrypted_aes_key)

    #     # Compare original and decrypted files
    #     self.assertTrue(filecmp.cmp(original_file_path, decrypted_file_path),
    #                     "Decrypted file does not match the original.")

    #     # Cleanup: remove the encrypted and decrypted files
    #     os.remove(encrypted_file)
    #     os.remove(decrypted_file_path)


if __name__ == '__main__':
    unittest.main()
