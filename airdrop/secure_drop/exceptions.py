class ContactAlreadyAddedException(Exception):
    """Raised when the user attempts to add a contact that's already been added."""


class MissingCredentialsException(Exception):
    """Raised when a client attempts to retrieve the logged in user's credentials and they don't exist."""


class MissingFieldsException(Exception):
    """Raised when a received message is missing expected fields."""
