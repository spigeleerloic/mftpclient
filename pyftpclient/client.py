import ftplib
import argparse
import socket
import errno
import sys

# On Python 3.10 and above, socket.IPPROTO_MPTCP is defined.
# If not, we set it manually
try:
  IPPROTO_MPTCP = socket.IPPROTO_MPTCP
except AttributeError:
  IPPROTO_MPTCP = 262

# By default, the application wishes to use Multipath TCP for all sockets
# provided that it is running on a system that supports Multipath TCP
_use_mptcp = True

class FTPClient(ftplib.FTP):

    def __init__(self, host='', user='', passwd='', acct='', timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, *, encoding='utf-8'):
            super().__init__(host, user, passwd, acct, timeout, source_address, encoding=encoding)

    def get_socket(self, af, socktype):
        global _use_mptcp
        global IPPROTO_MPTCP
        # If Multipath TCP is enabled on this system, we create a Multipath TCP
        # socket
        if _use_mptcp and socktype == socket.SOCK_STREAM:  
            try:
                return socket.socket(af, socktype, IPPROTO_MPTCP)
            except socket.error as e:
                # Multipath TCP is not supported, we fall back to regular TCP
                # and remember that Multipath TCP is not enabled
                if e.errno == errno.ENOPROTOOPT or e.errno == errno.ENOPROTONOSUPPORT :
                    _use_mptcp = False
                
        # Multipath TCP does not work or socket failed, we try TCP
        return socket.socket(af, socktype, socket.IPPROTO_TCP)

    def create_connection(self, address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        host, port = address
        err = None
        for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = self.get_socket(af, socktype)
                if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                    sock.settimeout(timeout)
                if source_address:
                    sock.bind(source_address)
                sock.connect(sa)
                # Break explicitly a reference cycle
                err = None
                return sock

            except socket.error as _:
                err = _
                if sock is not None:
                    sock.close()

        if err is not None:
            try:
                raise err
            finally:
                # Break explicitly a reference cycle
                err = None
        else:
            raise socket.error("getaddrinfo returns an empty list")


    def connect(self, host='', port=0, timeout=-999, source_address=None):
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        if self.timeout is not None and not self.timeout:
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        if source_address is not None:
            self.source_address = source_address
        sys.audit("ftplib.connect", self, self.host, self.port)
        self.sock = self.create_connection((self.host, self.port), self.timeout, source_address=self.source_address)
        self.af = self.sock.family
        self.file = self.sock.makefile('r', encoding=self.encoding)
        self.welcome = self.getresp()
        return self.welcome

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default='127.0.0.1', type=str, help="The hostname of the server")
    parser.add_argument("--port", default=21, type=int, help="The port of the FTP server")
    client = FTPClient()
    args = parser.parse_args()
    client.connect(args.host, args.port)
    client.login()
    client.retrlines('LIST')
    client.quit()