#!/usr/bin/python

import socket
import argparse
import random
import string


from mftpclient.client import FTPClient
from mftpclient.test import unittest
from mftpclient._compat import is_mptcp_supported_on_sytem
from mftpclient.mptcp_support import get_mptcp_socket
from mftpclient.test.test_server import get_mptcp_server_socket


# TODO add more tests

class MPTCPSocketTestIPv4(unittest.TestCase):

    @unittest.skipIf(not is_mptcp_supported_on_sytem(), "Host OS doesn't support MPTCP")
    def test_mptcp_ipv4_socket_on_system(self):
        _server_sock = None
        _client_sock = None
        
        try:
            _server_sock, _server_used_mptcp = get_mptcp_server_socket(af=socket.AF_INET6)
            _client_sock, _client_used_mptcp = get_mptcp_socket(af=socket.AF_INET6)

            _client_sock.connect(_server_sock.getsockname())
            text_length = 1024
            random_text = "".join(random.choice(string.ascii_letters) for _ in range(text_length))
            _client_sock.sendall(str.encode(random_text))
            conn, addr = _server_sock.accept()
            with conn:
                recv_text   = conn.recv(text_length).decode()
            self.assertEqual(random_text, recv_text)
            self.assertEqual(addr, _client_sock.getsockname())
            
        finally:
            _server_sock.close()
            _client_sock.close()

class MPTCPSocketTestIPv6(unittest.TestCase):

    @unittest.skipIf(not is_mptcp_supported_on_sytem(), "Host OS doesn't support MPTCP")
    def test_mptcp_ipv6_socket_on_system(self):
        _server_sock = None
        _client_sock = None
        try:
            _server_sock, _server_used_mptcp = get_mptcp_server_socket(af=socket.AF_INET6)
            _client_sock, _client_used_mptcp = get_mptcp_socket(af=socket.AF_INET6)

            _client_sock.connect(_server_sock.getsockname())
            text_length = 1024
            random_text = "".join(random.choice(string.ascii_letters) for _ in range(text_length))
            _client_sock.sendall(str.encode(random_text))
            conn, addr = _server_sock.accept()
            with conn:
                recv_text   = conn.recv(text_length).decode()
            self.assertEqual(random_text, recv_text)
            self.assertEqual(addr, _client_sock.getsockname())
            
        finally:
            _server_sock.close()
            _client_sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Enables verbose mode")
    args = parser.parse_args()
    unittest.main(verbosity=args.verbose)