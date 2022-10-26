from socket import socket
from mftpclient._compat import IS_PY3


if IS_PY3:
    import unittest
else:
    import unittest2 as unittest # requires "pip install unittest2"
