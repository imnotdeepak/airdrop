import socket
import uuid


class Connection:
    def __init__(self, app_uuid: uuid.UUID, email: str, sock: socket.socket):
        self.app_uuid: uuid.UUID = app_uuid
        self.email: str = email
        self.sock: socket.socket = sock
