#!/usr/bin/env python3

import sys
import socket
import argparse
print(sys.path)

from mftpclient.tests import unittest
from mftpclient.tests import PyftpclientTestCase

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
    parser.add_argument("-v", "verbose", action='store_true', help="Enables debug mode")
    args = parser.parse_args()
    unittest.main(verbosity=args.verbose)