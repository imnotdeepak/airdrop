import re
from getpass import getpass
from typing import Tuple

from secure_drop import constants, utils
from secure_drop.types.Credentials import Credentials


def get_credentials_for_registration() -> Credentials:
    """Prompts the user for all required credentials, validates them, and encrypts the password.

    Returns:
        Credentials: The validated credentials (password encrypted).
    """

    name = get_name_for_registration()
    email = get_email_for_registration()
    password = get_password_for_registration()
    return Credentials(name, email, password)


def get_name_for_registration() -> str:
    """Prompts the user for their full name and validates its length.

    Returns:
        str: The user's validated full name.
    """

    while True:
        name = input("Enter full name: ")
        if len(name) >= constants.MIN_NAME_LENGTH:
            break
        print(f"Your full name must contain at least {constants.MIN_NAME_LENGTH} characters. Please try again.")

    return name


def get_email_for_registration() -> str:
    """Prompts the user for their email and validates it using a tested regular expression.

    Returns:
        str: The user's validated email.
    """

    while True:
        email = input("Enter email address: ")
        if utils.is_valid_email(email):
            break
        print("Please enter a valid email address.")

    return email


def get_password_for_registration() -> str:
    """Prompts the user for a password, prompts them to confirm said password, and validates the length of the password.

    Returns:
        str: The user's validated password.
    """

    while True:
        password = getpass("Enter password: ")
        password_confirmation = getpass("Re-enter password: ")
        if password != password_confirmation:
            print("Passwords do not match. Please try again.")
        elif len(password) < constants.MIN_PASSWORD_LENGTH:
            print(f"Your password must contain at least {constants.MIN_PASSWORD_LENGTH} characters. Please try again.")
        else:
            print("Passwords match.")
            break

    return password


def get_email_and_password_for_login() -> Tuple[str, str]:
    """Prompts the user to enter their email and password for a login attempt.

    Returns:
        Tuple[str, str]: email, password
    """

    email = input("Enter email address: ")
    password = getpass("Enter password: ")
    return (email, password)
