import threading
from typing import Optional

from secure_drop import constants, utils
from secure_drop.types.Credentials import Credentials


class LoginManager:
    """A thread-safe singleton responsible for managing user login across SecureDrop."""

    _instance: Optional["LoginManager"] = None
    _lock: threading.Lock = threading.Lock()
    _login_attempts: int = 0 
    _logged_in: bool = False
    _max_login_attempts_exceeded: bool = False
    _logged_in_user_credentials: Optional[Credentials] = None

    def __new__(cls):
        """This method definition makes the class a singleton.
        """

        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LoginManager, cls).__new__(cls)
            return cls._instance

    def login_user(self, email: str, password: str):
        """Attempts to log the user in given an entered email and password. The singleton instance will remember failed login attempts and
        will return early from this method when the maximum number of failed login attempts have been exceeded. 

        Args:
            email (str): The user's enetered email.
            password (str): The user's entered password.
        """

        # Ensure that the maximum number of login attempts haven't been execeeded
        if self._max_login_attempts_exceeded:
            self.__print_max_login_attempts_exceeded_message()
            return

        credentials = LoginManager.__get_registered_user_credentials()
        if LoginManager.__credentials_valid(credentials, email, password):
            print("Email and password combination valid.")
            self._login_attempts = 0
            self._logged_in = True 
            self._logged_in_user_credentials = credentials
        else:
            print("Email and password combination invalid.")
            self._logged_in = False
            self._login_attempts += 1
            if self._login_attempts == constants.MAX_LOGIN_ATTEMPTS:
                self._max_login_attempts_exceeded = True
                self.__print_max_login_attempts_exceeded_message()

    def logged_in(self) -> bool:
        return self._logged_in

    def max_login_attempts_exceeded(self) -> bool:
        return self._max_login_attempts_exceeded

    def get_logged_in_user_credentials(self) -> Optional[Credentials]:
        return self._logged_in_user_credentials

    def clear(self):
        """Deletes the singleton instance.
        """

        self._login_attempts = 0 
        self._logged_in = False
        self._max_login_attempts_exceeded = False
        self._logged_in_user_credentials = None
        with self._lock:
            self._instance = None

    @staticmethod
    def __print_max_login_attempts_exceeded_message():
        print("Maximum number of login attempts exceeded.")

    @staticmethod
    def __get_registered_user_credentials() -> Credentials:
        """Retrieves the credentials of the registered user.

        Raises:
            RuntimeError: Raised if no user has been registered with SecureDrop.

        Returns:
            Credentials: The credentials of the registered user.
        """

        if not utils.user_registered():
            raise RuntimeError("No user has been registered; unable to login user.")

        with open(constants.USER_FILE_PATH, "rb") as f:
            encrypted_json = f.read()
            f.close()

        return Credentials.from_encrypted_json(encrypted_json)

    @staticmethod
    def __credentials_valid(credentials: Credentials, entered_email: str, entered_password: str) -> bool:
        """Determines whether an entered email and password represent valid credentials given a registered user's known credentials.

        Args:
            credentials (Credentials): The registered user's known credentials.
            entered_email (str): The email entered by the user.
            entered_password (str): The password entered by the user.

        Returns:
            bool: True if the entered credentials are valid; False otherwise.
        """

        return entered_email == credentials.email and entered_password == credentials.password 
