import socket
import threading
import time
from typing import Optional

from secure_drop import constants
from secure_drop.networking.messages.BroadcastMessage import BroadcastMessage
from secure_drop.networking.NetworkResource import NetworkResource


class Broadcaster(NetworkResource):
    def __init__(self):
        super().__init__()
        self.__message: Optional[BroadcastMessage] = None
        self.__message_lock: threading.Lock = threading.Lock()
        self._add_thread(threading.Thread(target=self.__broadcast))

    def set_message(self, message: BroadcastMessage):
        with self.__message_lock:
            self.__message = message

    def __broadcast(self):
        with self.__create_broadcast_socket() as broadcast_socket:
            while True:
                with self._should_stop_lock:
                    if self._should_stop:
                        break
                with self.__message_lock:
                    if not self.__message:
                        continue
                    broadcast_socket.sendto(self.__message.to_bytes(), ("255.255.255.255", constants.BROADCAST_PORT))
                time.sleep(constants.BROADCAST_DELAY_SECONDS)

    @staticmethod
    def __create_broadcast_socket() -> socket.socket:
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return broadcast_socket
