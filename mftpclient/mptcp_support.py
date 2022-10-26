import socket
import errno

try:
  IPPROTO_MPTCP = socket.IPPROTO_MPTCP
except AttributeError:
  IPPROTO_MPTCP = 262

USE_MPTCP = True

def get_mptcp_socket(af = socket.AF_INET, socktype = socket.SOCK_STREAM):
  global USE_MPTCP
  global IPPROTO_MPTCP
  # If Multipath TCP is enabled on this system, we create a Multipath TCP
  # socket
  if USE_MPTCP and socktype == socket.SOCK_STREAM:  
      try:
          return socket.socket(af, socktype, IPPROTO_MPTCP), True
      except socket.error as e:
          # Multipath TCP is not supported, we fall back to regular TCP
          # and remember that Multipath TCP is not enabled
          if e.errno == errno.ENOPROTOOPT or e.errno == errno.ENOPROTONOSUPPORT :
              USE_MPTCP = False
          
  # Multipath TCP does not work or socket failed, we try TCP
  return socket.socket(af, socktype, socket.IPPROTO_TCP), False
