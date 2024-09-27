from secure_drop import constants
from secure_drop.types.Credentials import Credentials


def register_user(credentials: Credentials):
    """Registers a user with SecureDrop.

    Args:
        credentials (Credentials): The user's credentials.
    """

    credentials_json = credentials.to_encrypted_json()
    with open(constants.USER_FILE_PATH, "wb") as f:
        f.write(credentials_json)
