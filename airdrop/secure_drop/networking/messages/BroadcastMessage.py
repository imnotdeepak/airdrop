import json
import uuid

from secure_drop import exceptions
from secure_drop.networking.messages.Message import Message


class BroadcastMessage(Message):
    UUID_FIELD_NAME = "uuid"
    SERVER_IP_FIELD_NAME = "server_ip"
    SERVER_PORT_FIELD_NAME = "server_port"

    def __init__(self, app_uuid: uuid.UUID, server_ip: str, server_port: int):
        self.app_uuid: uuid.UUID = app_uuid
        self.server_ip: str = server_ip
        self.server_port: int = server_port

    def to_bytes(self) -> bytes:
        return json.dumps({
            f"{self.UUID_FIELD_NAME}": f"{self.app_uuid}",
            f"{self.SERVER_IP_FIELD_NAME}": f"{self.server_ip}",
            f"{self.SERVER_PORT_FIELD_NAME}": self.server_port
        }).encode()

    @classmethod
    def from_bytes(cls, data: bytes) -> "BroadcastMessage":
        json_data = json.loads(data.decode())
        if BroadcastMessage.UUID_FIELD_NAME not in json_data or \
            BroadcastMessage.SERVER_IP_FIELD_NAME not in json_data or \
            BroadcastMessage.SERVER_PORT_FIELD_NAME not in json_data:
            raise exceptions.MissingFieldsException()
        other_uuid = uuid.UUID(json_data[BroadcastMessage.UUID_FIELD_NAME])
        other_server_ip = json_data[BroadcastMessage.SERVER_IP_FIELD_NAME]
        other_server_port = json_data[BroadcastMessage.SERVER_PORT_FIELD_NAME]
        return BroadcastMessage(other_uuid, other_server_ip, other_server_port)
