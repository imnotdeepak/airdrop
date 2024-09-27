class Contact:
    def __init__(self, name: str, email: str):
        self.name: str = name
        self.email: str = email

    def __eq__(self, other: object) -> bool:
        """Determines if a given object is equal to the contact.

        Args:
            other (object): The object to compare to the contact.

        Returns:
            bool: True if the object is equal to the contact; False otherwise.
        """

        if isinstance(other, Contact):
            return self.email.lower() == other.email.lower()

        return False

    def __str__(self) -> str:
        """Returns the string representation of a contact.

        Returns:
            str: The string representation of the contact.
        """

        return f"{self.name} <{self.email}>" 
