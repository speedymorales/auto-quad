#!/usr/bin/env python

from threading import Thread
import socket
import serial
import time
import struct
import sys
import numpy as np
import pandas as pd

class SocketRead:
    def __init__(self, host='proxy.jlmo.info', port=9999):
        
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.host = host
      self.port = port

      self.rawData = []
      self.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

      self.isRun = True
      self.isReceiving = False
      self.thread = None

      print('Trying to connect to: ' + self.host + ':' + str(self.port))
      try:
        self.sock.connect((self.host, self.port))
      except socket.error as exc:
        print("Caught exception socket.error : %s" % exc)
        exit()

    def readSocketStart(self):
      if self.thread == None:
        self.thread = Thread(target=self.backgroundThread)
        self.thread.start()
        # Block till we start receiving values
        while self.isReceiving != True:
          time.sleep(0.1)

    def getSocketData(self):
      privateData = self.rawData[:]
      
      self.data = []
      # gyro
      self.data.append(((privateData[0] * 0.00875) - 0.464874541896) / 180.0 * np.pi)
      self.data.append(((privateData[1] * 0.00875) - 9.04805461852) / 180.0 * np.pi)
      self.data.append(((privateData[2] * 0.00875) - 0.23642053973) / 180.0 * np.pi)
      # accelerometer
      self.data.append((privateData[3] * 0.061) - 48.9882695319)
      self.data.append((privateData[4] * 0.061) - 58.9882695319)
      self.data.append((privateData[5] * 0.061) - 75.9732905214)
      # magnetometer
      self.data.append(privateData[6] * 0.080)
      self.data.append(privateData[7] * 0.080)
      self.data.append(privateData[8] * 0.080)

      return self.data

    def backgroundThread(self):    # retrieve data
      while (self.isRun):
        # Receive 6 bytes
        msg = self.sock.recv(6)
        header = msg[0:4].decode()

        if header == 'DATA':

          self.rawData = []

          size = struct.unpack('H', msg[4:6])[0]
          msg = self.sock.recv(size)
          # print([ "0x%02x" % b for b in msg ])

          print('----------')
          for i in range(0, int(size/8)):
            unpackedFloat = struct.unpack('d', msg[i*8: i*8+8])[0]
            self.rawData.append(unpackedFloat)
            print(unpackedFloat)
        
          sys.stdout.flush()
        
        # time.sleep(1.0)  # give some buffer time for retrieving data

    def close(self):
      self.isRun = False
      self.thread.join()
      self.sock.close()
      print('Disconnected...')
      # df = pd.DataFrame(self.csvData)
      # df.to_csv('/home/rikisenia/Desktop/data.csv')