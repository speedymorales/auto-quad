#!/usr/bin/python3           # This is server.py file
import socket
import sys
import netifaces as ni
import struct

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
# host = '127.0.0.1' #socket.gethostname()

# ni.ifaddresses('wlan0')
# host = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
host = 'localhost'

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
# serversocket.listen(5)
serversocket.listen()

while True:
   # establish a connection
   clientsocket, addr = serversocket.accept()

   print("Got a connection from %s" % str(addr))
   
   msg = 'Thank you for connecting'+ "\r\n"
   msg = bytearray()
   msg.extend('DATA'.encode())

   value = [float(5.10001), float(600.0), float(123.45), float(100), float(0), float(1.1), float(24.25), float(0.001), float(1.112)]

   datagram = b''
   for f in value:
      datagram = datagram + struct.pack("d", f)
   
   print([ "0x%02x" % b for b in datagram ])
   print(len(datagram))

   msg = msg + struct.pack('H', len(datagram))
   msg = msg + datagram

   clientsocket.send(msg)

   sys.stdout.flush()
   clientsocket.close()