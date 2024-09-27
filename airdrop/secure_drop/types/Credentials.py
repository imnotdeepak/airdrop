import json

from secure_drop import crypto


class Credentials:
    """Encapsulates a user's credentials. Instances of this class are serialized to JSON and written to a file.
    """

    def __init__(self, name: str, email: str, password: str):
        self.name: str = name
        self.email: str = email
        self.password: str = password

    def to_encrypted_json(self) -> bytes:
        """Converts the contact into encrypted JSON.

        Returns:
            bytes: The encrypted JSON.
        """

        json_data = json.dumps(self.__dict__)
        return crypto.encrypt_RSA(json_data.encode())

    @staticmethod
    def from_encrypted_json(encrypted_json: bytes) -> "Credentials":
        """Constructs a new credentials object from encrypted JSON.

        Args:
            encrypted_json (bytes): The encrypted JSON used to initialize the credentials object.

        Returns:
            Credentials: The newly constructed credentials object.
        """

        decrypted_json = crypto.decrypt_RSA(encrypted_json)
        json_data = json.loads(decrypted_json)
        return Credentials(**json_data)
