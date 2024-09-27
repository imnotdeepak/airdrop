import os
import re

from secure_drop import constants


def user_registered() -> bool:
    """Determines whether a user has been registered with SecureDrop.

    Returns:
        bool: True if a user has been registered; False otherwise.
    """

    return os.path.exists(constants.USER_FILE_PATH)


def contacts_file_exists() -> bool:
    """Determines whether the contacts file exists.

    Returns:
        bool: True if the contacts file exists, False otherwise
    """

    return os.path.exists(constants.CONTACTS_FILE_PATH)


def is_valid_email(string: str) -> bool:
    """Determines whether a given string represents a valid email address.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the given string represents a valid email address; False otheriwse.
    """

    return re.match(constants.EMAIL_REGEX, string)
