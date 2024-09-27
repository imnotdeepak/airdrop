import json

from secure_drop import exceptions
from secure_drop.networking.messages.Message import Message


class ServerResponse(Message):
    STR_RES_FIELD_NAME = "str_res"
    BOOL_RES_FIELD_NAME = "bool_res"

    def __init__(self, str_res: str = "", bool_res: bool = False):
        super().__init__()
        self.str_res: str = str_res
        self.bool_res: bool = bool_res

    def to_bytes(self) -> bytes:
        return json.dumps({
            f"{self.STR_RES_FIELD_NAME}": f"{self.str_res}",
            f"{self.BOOL_RES_FIELD_NAME}": self.bool_res
        }).encode()

    @classmethod
    def from_bytes(cls, data: bytes) -> "ServerResponse":
        json_data = json.loads(data.decode())
        if ServerResponse.STR_RES_FIELD_NAME not in json_data or ServerResponse.BOOL_RES_FIELD_NAME not in json_data:
            raise exceptions.MissingFieldsException()
        str_res = json_data[ServerResponse.STR_RES_FIELD_NAME]
        bool_res = json_data[ServerResponse.BOOL_RES_FIELD_NAME]
        return ServerResponse(str_res, bool_res)
