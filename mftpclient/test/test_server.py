import socket
from mftpclient.mptcp_support import IPPROTO_MPTCP
from mftpclient.mptcp_support import get_mptcp_socket

def get_mptcp_server_socket(af = socket.AF_INET, type=socket.SOCK_STREAM):
    server_socket, used_mptcp = get_mptcp_socket(af, type)
    server_socket.bind(('', 0))
    server_socket.listen()
    return server_socket, used_mptcp
