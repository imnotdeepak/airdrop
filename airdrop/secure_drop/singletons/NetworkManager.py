import threading
from typing import Optional

from secure_drop import constants
from secure_drop.networking.Broadcaster import Broadcaster
from secure_drop.networking.BroadcastListener import BroadcastListener
from secure_drop.networking.messages.BroadcastMessage import BroadcastMessage
from secure_drop.networking.TCPServer import TCPServer
from secure_drop.types.Contact import Contact


class NetworkManager:
    _instance: Optional["NetworkManager"] = None
    _instance_lock: threading.Lock = threading.Lock()
    _tcp_server: TCPServer = TCPServer()
    _broadcaster: Broadcaster = Broadcaster()
    _broadcast_listener: BroadcastListener = BroadcastListener()

    def __new__(cls):
        """This method definition makes the class a singleton.
        """

        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(NetworkManager, cls).__new__(cls)
            return cls._instance

    def start(self):
        self._tcp_server.start()
        while (server_port := self._tcp_server.get_port()) is None:
            pass
        broadcast_message = BroadcastMessage(constants.APP_UUID, constants.SERVER_IP, server_port)
        self._broadcaster.set_message(broadcast_message)
        self._broadcaster.start()
        self._broadcast_listener.start()

    def stop(self):
        self._broadcast_listener.stop()
        self._broadcaster.stop()
        self._tcp_server.stop()

    def clear(self):
        self.stop()
        with self._instance_lock:
            self._instance = None

    def contact_has_reciprocated(self, contact: Contact) -> bool:
        return self._broadcast_listener.contact_has_reciprocated(contact)

    def send_file(self, contact: Contact, file_path: str) -> bool:
        return self._broadcast_listener.send_file(contact, file_path)

    def is_waiting_for_send_file_consent(self) -> bool:
        return self._tcp_server.is_waiting_for_send_file_consent()

    def consent_to_receive_file(self):
        self._tcp_server.consent_to_receive_file()

    def reject_receiving_file(self):
        self._tcp_server.reject_receiving_file()
