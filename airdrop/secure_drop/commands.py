from secure_drop import exceptions, input_helpers
from secure_drop.singletons.ContactManager import ContactManager
from secure_drop.singletons.NetworkManager import NetworkManager
from secure_drop.types.Contact import Contact
from secure_drop.types.ContactList import ContactList


def help():
    """Displays the help menu.
    """

    print("\"add\"  -> Add a new contact")
    print("\"list\" -> List all online contacts")
    print("\"send\" -> Transfer file to contact")
    print("\"exit\" -> Exit SecureDrop")


def add_contact():
    """Prompts the user to enter a name and email for a contact they wish to add, then attempts to add this contact.
    """

    name = input_helpers.get_name_for_registration()
    email = input_helpers.get_email_for_registration()
    contact = Contact(name, email)

    try:
        ContactManager().add_contact(contact)
        print(f"Contact {contact} added successfully.")
    except exceptions.ContactAlreadyAddedException:
        print(f"Contact {contact} has already been added.")


def list_contacts():
    # 1. Retrieve contacts that have already been added
    contacts = ContactManager().get_contacts()

    # 2. For each contact, determine if they should be listed
    contacts_to_list = ContactList()
    network_manager = NetworkManager()
    for contact in contacts:
        if network_manager.contact_has_reciprocated(contact):
            contacts_to_list.add_contact(contact)
    
    # 3. Display the relevant contacts
    if any(contacts_to_list):
        print("The following contacts are online:")
        for contact in contacts_to_list:
            print(f"* {contact}")
    else:
        print("No contacts are currently online.")


def send_file(email: str, file_path: str):
    contacts = ContactManager().get_contacts()
    if (target_contact := contacts.get_contact_by_email(email)) is None:
        print(f"Unable to send file: you haven't added {email} as a contact.")
        return
    if not NetworkManager().contact_has_reciprocated(target_contact):
        print(f"Unable to send file: {target_contact} has not added you as a contact or is not online.")
        return
    if NetworkManager().send_file(target_contact, file_path):
        print("Sent file successfully.")
    else:
        print("Failed to send file.")
