#!/usr/bin/python3           # This is client.py file

import socket
import struct
import sys

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# tst = 5.123
# print(type(tst))
# print(tst)

# host = socket.gethostname()
host = 'proxy.jlmo.info'
host = 'localhost'

port = 9999

# connection to hostname on the port.
s.connect((host, port))

# Receive no more than 1024 bytes
msg = s.recv(6)
print([ "0x%02x" % b for b in msg ])
# sys.stdout.flush()

header = msg[0:4].decode()
print(header)

if header == 'DATA':
  size = struct.unpack('H', msg[4:6])[0]
  print(size)
  msg = s.recv(size)
  print([ "0x%02x" % b for b in msg ])

  for i in range(0, int(size/8)):
    print(struct.unpack('d', msg[i*8: i*8+8])[0])

  # print([ "0x%02x" % b for b in msg[0:8] ])
  # print(struct.unpack("d", msg[0:8])[0])

  # print([ "0x%02x" % b for b in msg[8:16] ])
  # print(struct.unpack("d", msg[8:16])[0])

  s.close()
  # print (msg.decode('ascii'))
