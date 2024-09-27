from abc import ABC, abstractclassmethod, abstractmethod


class Message(ABC):
    # TODO: Cryptography
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractclassmethod
    def from_bytes(cls, data: bytes) -> "Message":
        pass
