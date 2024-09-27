import platform
import socket
import threading
import time
import uuid
from typing import List, Optional

from secure_drop import constants, exceptions
from secure_drop.networking import socket_helpers
from secure_drop.networking.Connection import Connection
from secure_drop.networking.messages.BroadcastMessage import BroadcastMessage
from secure_drop.networking.NetworkResource import NetworkResource
from secure_drop.singletons.LoginManager import LoginManager
from secure_drop.types.Contact import Contact


class BroadcastListener(NetworkResource):
    def __init__(self):
        super().__init__()
        self.__connections: List[Connection] = []
        self.__connections_lock: threading.Lock = threading.Lock()
        self._add_thread(threading.Thread(target=self.__listen))
        self._add_thread(threading.Thread(target=self.__update_connections))

    def stop(self):
        super().stop()
        # Close all connected sockets
        with self.__connections_lock:
            for connection in self.__connections:
                connection.sock.close() 

    def contact_has_reciprocated(self, contact: Contact) -> bool:
        if (connection := self.__get_connection_by_email(contact.email)) is None:
            return False
        if (logged_in_user_credentials := LoginManager().get_logged_in_user_credentials()) is None:
            raise exceptions.MissingCredentialsException()
        if (ret := socket_helpers.has_added_user(connection.sock, logged_in_user_credentials.email)) is None:
            self.__remove_connections([connection])
            return False
        return ret

    def send_file(self, contact: Contact, file_path: str) -> bool:
        if (connection := self.__get_connection_by_email(contact.email)) is None or \
            not socket_helpers.consents_to_receive_file(connection.sock) or \
            not socket_helpers.send_file(connection.sock, file_path):
            return False
        return True

    def __listen(self):
        with self.__create_listener_socket() as listener_socket:
            while True:
                with self._should_stop_lock:
                    if self._should_stop:
                        break
                message = listener_socket.recv(1024)
                broadcast_message = BroadcastMessage.from_bytes(message)
                # Do nothing if the broadcast is this app instance's own or if it's already connected to the other instance
                if broadcast_message.app_uuid == constants.APP_UUID or self.__contains_connection(broadcast_message.app_uuid):
                    continue
                self.__connect(broadcast_message.app_uuid, broadcast_message.server_ip, broadcast_message.server_port)

    def __connect(self, app_uuid: uuid.UUID, server_ip: str, server_port: int):
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((server_ip, server_port))
        conn_email = socket_helpers.get_email(conn_socket)
        if conn_email is None:
            conn_socket.close()
            return
        connection = Connection(app_uuid, conn_email, conn_socket)
        self.__add_connection(connection)

    def __update_connections(self):
        while True:
            with self._should_stop_lock:
                if self._should_stop:
                    break
            with self.__connections_lock:
                connections_to_remove: List[uuid.UUID] = []
                for connection in self.__connections:
                    if not socket_helpers.is_connected_to(connection.sock):
                        connections_to_remove.append(connection.app_uuid)
            self.__remove_connections(connections_to_remove)
            time.sleep(constants.CONNECTIONS_UPDATE_DELAY_SECONDS)

    def __add_connection(self, connection: Connection):
        with self.__connections_lock:
            self.__connections.append(connection)

    def __remove_connections(self, connections: List[Connection]):
        with self.__connections_lock:
            self.__connections = list(filter(lambda c: c.app_uuid not in connections, self.__connections))

    def __contains_connection(self, app_uuid: uuid.UUID):
        with self.__connections_lock:
            for connection in self.__connections:
                if connection.app_uuid == app_uuid:
                    return True
        return False

    def __get_connection_by_email(self, email: str) -> Optional[Connection]:
        with self.__connections_lock:
            for connection in self.__connections:
                if connection.email == email:
                    return connection
        return None

    @staticmethod
    def __create_listener_socket() -> socket.socket:
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if platform.system() == "Windows":
            listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        listener_socket.bind(("", constants.BROADCAST_PORT))
        listener_socket.setsockopt(
            socket.IPPROTO_IP, 
            socket.IP_ADD_MEMBERSHIP, 
            socket.inet_aton(constants.MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
        )
        return listener_socket
