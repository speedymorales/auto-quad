#!/usr/bin/python3           # This is server.py file
import socket
import sys
import netifaces as ni
import struct
import time
from threading import Thread

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
   
   # for i in range(0, 5):
   while True:
      msg = bytearray()
      msg.extend('DATA'.encode())

      rawData = [float(5.10001), float(600.0), float(123.45), float(100), float(0), float(1.1), float(24.25), float(0.001), float(1.112)]

      datagram = bytearray()
      for f in rawData:
         datagram = datagram + struct.pack("d", f)
      
      # print([ "0x%02x" % b for b in datagram ])
      # print(len(datagram))

      msg = msg + struct.pack('H', len(datagram))
      msg = msg + datagram
      clientsocket.send(msg)
      print("Message Sent to " + str(addr))

      sys.stdout.flush()

      time.sleep(.2)
   
   clientsocket.close()