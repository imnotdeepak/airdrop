import socket
import uuid


def __get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
            temp_socket.connect(("8.8.8.8", 80))
            return temp_socket.getsockname()[0]
    except OSError:
        return "127.0.0.1"


USER_FILE_PATH = "user.json"
PUBLIC_KEY_FILE_PATH = "public_key.pem"
PRIVATE_KEY_FILE_PATH = "private_key.pem"
MAX_LOGIN_ATTEMPTS = 5
MIN_NAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 8
# This ridiculous regex is RFC-5322-compliant and was obtained from here: https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
CONTACTS_FILE_PATH = "contacts.json"
BROADCAST_PORT = 9999
BROADCAST_DELAY_SECONDS = 1
CONNECTIONS_UPDATE_DELAY_SECONDS = 3
MULTICAST_GROUP = "224.1.1.1"
SERVER_IP = __get_local_ip()
SERVER_PORT_RANGE = range(1100, 1120)
APP_UUID = uuid.uuid4()
FILE_CHUNK_SIZE = 4096
RECEIVED_FILES_DIR = "received_files"
