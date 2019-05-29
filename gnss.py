#!/usr/bin/python3

import serial
from time import sleep

baud = bytearray([0xB5, 0x62, 0x06, 0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0xd0, 0x08, 0x00, 0x00, 0x00, 0xC2, 0x01, 0x00, 0x07, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC4, 0x96, 0xB5, 0x62, 0x06, 0x00, 0x01, 0x00, 0x01, 0x08, 0x22]) # 115200
rate = bytearray([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x7A, 0x12]) # (10Hz)

gll = bytearray([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x2B]) # GxGLL off
gsv = bytearray([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x39]) # GxGSV off
vtg = bytearray([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x05, 0x47]) # GxVTG off

save = bytearray([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0xC8, 0x00, 0x01, 0x00, 0x01, 0x00, 0xDE, 0x6A, 0xB5, 0x62, 0x06, 0x08, 0x00, 0x00, 0x0E, 0x30]) # save config in EEPROM

# gga = [0xB5,0x62,0x06,0x01,0x08,0x00,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x24] # GxGGA off
# gsa = [0xB5,0x62,0x06,0x01,0x08,0x00,0xF0,0x02,0x00,0x00,0x00,0x00,0x00,0x01,0x02,0x32] # GxGSA off

#ser = serial.Serial("/dev/serial0", 9600)
#ser.write(baud)
#ser.close()

ser = serial.Serial("/dev/serial0", 115200)

ser.write(gll)
ser.write(gsv)
ser.write(vtg)

ser.write(rate)

# ser.write(save)

print("Receiving Data")

def checksum( dataSet ):
  ck_a = 0
  ck_b = 0

  for i in range(2, len(dataSet)):
    ck_a = ck_a + dataSet[i]
    ck_b = ck_b + ck_a

while True:
  received_data = ser.readline()
  print (received_data)
