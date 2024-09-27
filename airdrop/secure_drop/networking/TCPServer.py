import os
import socket
import threading
import time
from typing import Optional

from secure_drop import constants, exceptions
from secure_drop.networking import socket_helpers
from secure_drop.networking.messages.ClientRequest import (ClientRequest,
                                                           ClientRequestType)
from secure_drop.networking.NetworkResource import NetworkResource
from secure_drop.singletons.ContactManager import ContactManager
from secure_drop.singletons.LoginManager import LoginManager
from secure_drop.types.Contact import Contact


class TCPServer(NetworkResource):
    def __init__(self):
        super().__init__()
        self.__port: Optional[int] = None
        self.__port_lock: threading.Lock = threading.Lock()
        self.__is_waiting_for_send_file_consent: bool = False
        self.__is_waiting_for_send_file_consent_lock: threading.Lock = threading.Lock()
        self.__consents_to_receive_file: bool = False
        self.__consents_to_receive_file_lock: threading.Lock = threading.Lock()
        self._add_thread(threading.Thread(target=self.__serve))

    def get_port(self) -> Optional[int]:
        with self.__port_lock:
            return self.__port

    def is_waiting_for_send_file_consent(self) -> bool:
        with self.__is_waiting_for_send_file_consent_lock:
            return self.__is_waiting_for_send_file_consent

    def consent_to_receive_file(self):
        with self.__consents_to_receive_file_lock:
            self.__consents_to_receive_file = True
        with self.__is_waiting_for_send_file_consent_lock:
            self.__is_waiting_for_send_file_consent = False

    def reject_receiving_file(self):
        with self.__consents_to_receive_file_lock:
            self.__consents_to_receive_file = False
        with self.__is_waiting_for_send_file_consent_lock:
            self.__is_waiting_for_send_file_consent = False

    def __serve(self):
        with self.__create_server_socket() as server_socket:
            while True:
                with self._should_stop_lock:
                    if self._should_stop:
                        break
                try:
                    conn_socket, _ = server_socket.accept()
                    conn_thread = threading.Thread(target=self.__handle_client_connection, args=[conn_socket])
                    self._add_thread(conn_thread)
                    conn_thread.start()
                except BlockingIOError:
                    # No client attempted to connect => do nothing
                    pass

    def __create_server_socket(self) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(False)
        self.__bind_server_socket(server_socket)
        max_num_connections = constants.SERVER_PORT_RANGE.stop - constants.SERVER_PORT_RANGE.start
        server_socket.listen(max_num_connections)
        return server_socket

    def __bind_server_socket(self, server_socket: socket.socket):
        with self.__port_lock:
            for port in constants.SERVER_PORT_RANGE:
                try:
                    server_socket.bind((constants.SERVER_IP, port))
                    self.__port = port
                    break
                except OSError:
                    # A socket is already bound to the port => try the next one
                    pass
            if self.__port is None:
                raise RuntimeError("Unable to bind server socket: no available ports")                    

    def __handle_client_connection(self, conn_socket: socket.socket):
        with conn_socket:
            conn_socket.setblocking(False)
            while True:
                with self._should_stop_lock:
                    if self._should_stop:
                        break
                try:
                    data = conn_socket.recv(1024)
                    if not data:
                        # Empty data means the connection was closed
                        break
                    req = ClientRequest.from_bytes(data)
                    if not self.__handle_client_req(conn_socket, req):
                        # Unable to successfully handle the request => disconnect from the client
                        break
                except BlockingIOError:
                    # No data was received => do nothing
                    pass
                except OSError:
                    # The socket was disconnected
                    break

    def __handle_client_req(self, sock: socket.socket, req: ClientRequest) -> bool:
        ret = False
        req_type = ClientRequestType(req.type)
        if req_type == ClientRequestType.PING:
            ret = socket_helpers.send_ping_res(sock)
        elif req_type == ClientRequestType.EMAIL:
            logged_in_user_credentials = LoginManager().get_logged_in_user_credentials()
            if logged_in_user_credentials is None:
                raise exceptions.MissingCredentialsException()
            ret = socket_helpers.send_email_res(sock, logged_in_user_credentials.email)
        elif req_type == ClientRequestType.HAS_ADDED:
            email_to_check = req.args[0]
            contact_to_check = Contact("", email_to_check)
            has_added = ContactManager().get_contacts().contains(contact_to_check)
            ret = socket_helpers.send_bool_res(sock, has_added)
        elif req_type == ClientRequestType.SEND_FILE_CONSENT:
            sender_email = req.args[0]
            contact = ContactManager().get_contacts().get_contact_by_email(sender_email)
            if contact is None:
                ret = socket_helpers.send_bool_res(sock, False)
            else:
                self.__wait_for_send_file_consent(contact)
                with self.__consents_to_receive_file_lock:
                    ret = socket_helpers.send_bool_res(sock, self.__consents_to_receive_file)
        elif req_type == ClientRequestType.SEND_FILE:
            sock.setblocking(True)
            file_path = req.args[0]
            file_name = os.path.basename(file_path)
            if not os.path.isdir(constants.RECEIVED_FILES_DIR):
                os.makedirs(constants.RECEIVED_FILES_DIR)
            target_path = os.path.join(constants.RECEIVED_FILES_DIR, file_name)
            ret = socket_helpers.receive_file(sock, target_path)
            sock.setblocking(False)
        else:
            raise ValueError(f"Received unexpected enum value: {req.type}")
        return ret

    def __wait_for_send_file_consent(self, contact: Contact):
        with self.__is_waiting_for_send_file_consent_lock:
            self.__is_waiting_for_send_file_consent = True
        print(f"Contact {contact} is sending a file. Accept (y/n)?")
        while True:
            with self.__is_waiting_for_send_file_consent_lock:
                if not self.__is_waiting_for_send_file_consent:
                    break
            time.sleep(0.1)
