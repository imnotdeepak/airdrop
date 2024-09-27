import os
import socket
from typing import Optional

from secure_drop import constants
from secure_drop.networking.messages.ClientRequest import (ClientRequest,
                                                           ClientRequestType)
from secure_drop.networking.messages.ServerResponse import ServerResponse
from secure_drop.singletons.LoginManager import LoginManager


def is_connected_to(sock: socket.socket) -> bool:
    try:
        req = ClientRequest(ClientRequestType.PING)
        sock.sendall(req.to_bytes())
        _ = sock.recv(1024)
    except OSError: 
        return False 
    return True


def get_email(sock: socket.socket) -> Optional[str]:
    try:
        req = ClientRequest(ClientRequestType.EMAIL)
        sock.sendall(req.to_bytes())
        data = sock.recv(1024)
        res = ServerResponse.from_bytes(data)
        return res.str_res
    except OSError:
        return None


def has_added_user(sock: socket.socket, email: str) -> Optional[bool]:
    try:
        args = [email]
        req = ClientRequest(ClientRequestType.HAS_ADDED, args)
        sock.sendall(req.to_bytes())
        data = sock.recv(1024)
        res = ServerResponse.from_bytes(data)
        return res.bool_res
    except OSError:
        return None


def consents_to_receive_file(sock: socket.socket) -> bool:
    try:
        logged_in_user_credentials = LoginManager().get_logged_in_user_credentials()
        if not logged_in_user_credentials:
            return False
        # Send the logged in user's email so the connection so they know who the file is coming from
        args = [logged_in_user_credentials.email]
        req = ClientRequest(ClientRequestType.SEND_FILE_CONSENT, args)
        sock.sendall(req.to_bytes())
        data = sock.recv(1024)
        res = ServerResponse.from_bytes(data)
        return res.bool_res
    except OSError:
        return False


def send_file(sock: socket.socket, file_path: str) -> bool:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Unable to find file: {file_path}")
    try:
        args = [file_path]
        req = ClientRequest(ClientRequestType.SEND_FILE, args)
        sock.sendall(req.to_bytes())
        chunks = []
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(constants.FILE_CHUNK_SIZE)
                if not chunk:
                    break
                chunks.append(chunk)
        for chunk in chunks:
            sock.sendall(chunk)
            # Wait for an acknowledgement from the server
            _ = sock.recv(1024)
        sock.sendall(b"done sending")
    except OSError:
        return False
    return True


def receive_file(sock: socket.socket, file_path: str) -> bool:
    try:
        res = ServerResponse(str_res="acknowledgement")
        chunks = []
        while True:
            chunk = sock.recv(constants.FILE_CHUNK_SIZE)
            if not chunk or chunk == b"done sending":
                break
            chunks.append(chunk)
            # Send an acknowledgement to the client
            sock.sendall(res.to_bytes())
        with open(file_path, "wb") as f:
            for chunk in chunks:
                f.write(chunk)
    except OSError:
        return False
    return True


def send_ping_res(sock: socket.socket) -> bool:
    try:
        res = ServerResponse(str_res="ping")
        sock.sendall(res.to_bytes())
        return True
    except OSError:
        return False


def send_email_res(sock: socket.socket, email: str) -> bool:
    try:
        res = ServerResponse(str_res=email)
        sock.sendall(res.to_bytes())
        return True
    except OSError:
        return False


def send_bool_res(sock: socket.socket, boolean: bool) -> bool:
    try:
        res = ServerResponse(bool_res=boolean)
        sock.sendall(res.to_bytes())
        return True
    except OSError:
        return False
