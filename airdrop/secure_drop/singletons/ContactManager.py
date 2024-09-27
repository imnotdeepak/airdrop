import threading
from typing import Optional

from secure_drop import constants, exceptions, utils
from secure_drop.types.Contact import Contact
from secure_drop.types.ContactList import ContactList


class ContactManager:
    """A thread-safe singleton that's responsible for managing the user's global contact list.
    """

    _instance: Optional["ContactManager"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        """This method definition makes the class a singleton.
        """

        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ContactManager, cls).__new__(cls)
            return cls._instance

    def add_contact(self, contact: Contact):
        """_summary_

        Args:
            contact (Contact): _description_

        Raises:
            exceptions.ContactAlreadyAddedException: _description_
        """

        contacts = self.get_contacts()
        if contacts.contains(contact):
            raise exceptions.ContactAlreadyAddedException()

        contacts.add_contact(contact)
        self.__write_contacts_to_file(contacts)

    def get_contacts(self) -> ContactList:
        """Retrieves the list of contacts that have been added to SecureDrop from the contacts file. If the contacts
        file has not yet been created, this will return an empty list of contacts.

        Returns:
            ContactList: The list of contacts that have been added to SecureDrop.
        """

        if not utils.contacts_file_exists():
            return ContactList()

        return self.__read_contacts_from_file()

    def clear(self):
        """Deletes the singleton instance.
        """

        with self._lock:
            self._instance = None

    def __write_contacts_to_file(self, contacts: ContactList):
        """Encrypts a given list of contacts and writes it to the contacts file.

        Args:
            contacts (ContactList): The list of contacts to encrypt and write to the contacts file.
        """

        encrypted_json = contacts.to_encrypted_json()
        with open(constants.CONTACTS_FILE_PATH, "wb") as f:
            f.write(encrypted_json)
            f.close()

    def __read_contacts_from_file(self) -> ContactList:
        """Reads the list of contacts that have been added to SecureDrop out of the contacts file.

        Raises:
            RuntimeError: Raised if the contacts file does not exist.

        Returns:
            ContactList: The list of contacts added to SecureDrop.
        """

        if not utils.contacts_file_exists:
            raise RuntimeError("Contacts file does not exist.")
        with open(constants.CONTACTS_FILE_PATH, "rb") as f:
            encrypted_json = f.read()
        return ContactList.from_encrypted_json(encrypted_json)
