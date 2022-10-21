#!/usr/bin/python

import socket
import argparse

from mftpclient.test import unittest
from mftpclient.test import PyftpclientTestCase

if hasattr(socket, 'socketpair'):
    socketpair = socket.socketpair
else:
    # TODO : Implement our own version of socketpair
    print("Can't run tests without socketpair")
    exit(1)

class MPTCPSocketTesting(PyftpclientTestCase):
    def test_testWorking(self):
        self.assertTrue(hasattr(self, "_test_ctx"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Enables verbose mode")
    args = parser.parse_args()
    unittest.main(verbosity=args.verbose)