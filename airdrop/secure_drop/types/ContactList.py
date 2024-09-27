import json
from typing import List, Optional

from secure_drop import crypto
from secure_drop.types.Contact import Contact


class ContactList:
    def __init__(self):
        self.contacts: List[Contact] = []

    def __iter__(self):
        """This method override makes instances of the class iterable.
        """

        return iter(self.contacts)
       
    def add_contact(self, contact: Contact):
        """Adds a contact to the list.

        Args:
            contact (Contact): The contact to add to the list.
        """

        self.contacts.append(contact)

    def contains(self, contact: Contact) -> bool:
        """Determines whether the list contains a given contact.

        Args:
            contact (Contact): The contact to search the list for.

        Returns:
            bool: True if the given contact is found in the list; False otherwise.
        """

        return contact in self.contacts

    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        for contact in self.contacts:
            if contact.email == email:
                return contact
        return None

    def to_encrypted_json(self) -> bytes:
        """Converts the contact list into encrypted JSON.

        Returns:
            bytes: The encrypted JSON.
        """

        contacts_dicts = [vars(contact) for contact in self.contacts]
        contacts_json = json.dumps(contacts_dicts)
        return crypto.encrypt_RSA(contacts_json.encode())

    @staticmethod
    def from_encrypted_json(encrypted_json: bytes) -> "ContactList":
        """Constructs a new contact list from encrypted JSON.

        Args:
            encrypted_json (bytes): The encrypted JSON used to initialize the contact list.

        Returns:
            ContactList: The newly constructed contact list.
        """

        contacts_json = crypto.decrypt_RSA(encrypted_json)
        contacts_dicts = json.loads(contacts_json)
        contacts = [Contact(**data) for data in contacts_dicts]
        contact_list = ContactList()
        for contact in contacts:
            contact_list.add_contact(contact)

        return contact_list
