import json
from enum import Enum
from typing import List

from secure_drop import exceptions
from secure_drop.networking.messages.Message import Message


class ClientRequestType(Enum):
    PING = 0
    EMAIL = 1
    HAS_ADDED = 2
    SEND_FILE_CONSENT = 3
    SEND_FILE = 4


class ClientRequest(Message):
    TYPE_FIELD_NAME = "type"
    ARGS_FIELD_NAME = "args"

    def __init__(self, type: ClientRequestType, args: List[str] = []):
        self.type: ClientRequestType = type
        self.args: List[str] = args

    def to_bytes(self) -> bytes:
        return json.dumps({
            f"{self.TYPE_FIELD_NAME}": self.type.value,
            f"{self.ARGS_FIELD_NAME}": self.args
        }).encode()

    @classmethod
    def from_bytes(cls, data: bytes) -> "ClientRequest":
        json_data = json.loads(data.decode())
        if ClientRequest.TYPE_FIELD_NAME not in json_data or ClientRequest.ARGS_FIELD_NAME not in json_data:
            raise exceptions.MissingFieldsException() 
        req_type = json_data[ClientRequest.TYPE_FIELD_NAME]
        req_args = json_data[ClientRequest.ARGS_FIELD_NAME]
        return ClientRequest(req_type, req_args)
