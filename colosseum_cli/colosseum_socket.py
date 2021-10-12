import json
import socket
import os

from colosseum_cli import colosseum_cli_constants as con


def connect_and_send(json_data):
    """
    Connects to the specfied socket and writes the json message. returns reponse
    Args:
        socket_path:
        json_str:
    Returns:
    returns up to 1024 bytes worth of response
    """
    socket_path = con.SOCKET_PATH
    if os.environ.get(con.CLI_TEST_MODE_ENV) == 'TRUE':
        socket_path = con.TEST_SOCKET
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ret = {}
    try:
        # Connect to server and send data
        sock.connect(socket_path)
        json_str = json.dumps(json_data)
        sock.sendall(bytes(json_str, "utf-8"))
        # Receive data from the server and shut down
        received = str(sock.recv(3276800), "utf-8")
        ret = json.loads(received)

    except OSError as msg:
        print("ERROR: colosseumcli can not connect to server.")
    finally:
        sock.close()
    return ret
