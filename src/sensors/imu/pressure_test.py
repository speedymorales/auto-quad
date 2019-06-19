#!/usr/bin/python

import smbus
from time import sleep

bus = smbus.SMBus(1)

DEVICE_ADDRESS = 0x77      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d

BMP180_REG_CONTROL = 0xF4
BMP180_REG_RESULT = 0xF6

BMP180_COMMAND_TEMPERATURE = 0x2E
BMP180_COMMAND_PRESSURE_ULP = 0x34
BMP180_COMMAND_PRESSURE_STD = 0x74
BMP180_COMMAND_PRESSURE_HR = 0xB4
BMP180_COMMAND_PRESSURE_UHR = 0xF4

OSS = 0

#0 to 127 (lower half of a byte)
#0 to 32767 (lower half of a word)

def readWord(addr, cmd):
  global bus
  dSet = bus.read_i2c_block_data(addr, cmd)
  return dSet[0] << 8 | dSet[1]

def signedByte(byte):
  if byte > 127:
    return (256-byte) * (-1)
  else:
    return byte

def signedWord(word):
  if word > 32767:
    return (65536-word) * (-1)
  else:
    return word


def init():
  global AC1, AC2, AC3, AC4, AC5, AC6, B1, B2, MB, MC, MD

  AC1 = signedWord(readWord(DEVICE_ADDRESS, 0xAA))
  AC2 = signedWord(readWord(DEVICE_ADDRESS, 0xAC))
  AC3 = signedWord(readWord(DEVICE_ADDRESS, 0xAE))
  AC4 = readWord(DEVICE_ADDRESS, 0xB0)
  AC5 = readWord(DEVICE_ADDRESS, 0xB2)
  AC6 = readWord(DEVICE_ADDRESS, 0xB4)
  B1 = signedWord(readWord(DEVICE_ADDRESS, 0xB6))
  B2 = signedWord(readWord(DEVICE_ADDRESS, 0xB8))
  MB = signedWord(readWord(DEVICE_ADDRESS, 0xBA))
  MC = signedWord(readWord(DEVICE_ADDRESS, 0xBC))
  MD = signedWord(readWord(DEVICE_ADDRESS, 0xBE))

  print("AC1: " + str(AC1))
  print("AC2: " + str(AC2))
  print("AC3: " + str(AC3))
  print("AC4: " + str(AC4))
  print("AC5: " + str(AC5))
  print("AC6: " + str(AC6))
  print("B1: " + str(B1))
  print("B2: " + str(B2))
  print("MB: " + str(MB))
  print("MC: " + str(MC))
  print("MD: " + str(MD))
  print("---")
  print("")

init()

sleep(0.01)
while(True):
  
  bus.write_byte_data(DEVICE_ADDRESS, BMP180_REG_CONTROL, BMP180_COMMAND_TEMPERATURE) # Start a temperature reading
  sleep(0.005)
  tu = readWord(DEVICE_ADDRESS, BMP180_REG_RESULT) # Get the temperature reading

  # Calculating True Temperature
  X1 = (tu - AC6) * AC5 / float(32768)
  X2 = MC * float(2048) / (X1 + MD)
  B5 = X1 + X2
  T = (B5 + 8) / float(16)


  bus.write_byte_data(DEVICE_ADDRESS, BMP180_REG_CONTROL, BMP180_COMMAND_PRESSURE_ULP) # Start a pressure reading
  sleep(0.005)
  pu = readWord(DEVICE_ADDRESS, BMP180_REG_RESULT) # Get the pressure reading

  # Calculating True Pressure
  B6 = B5 - 4000
  X1 = ( B2 * ( (B6 * B6) / float(4096) ) ) / float(2048)
  X2 = (AC2 * B6) / float(2048)
  X3 = X1 + X2
  B3 = ( (AC1 << 2) + X3 + 2 ) / float(4)
  X1 = (AC3 * B6) / float(8192)
  X2 = ( B1 * ( B6 * B6 / float(4096) )) / float(65536)
  X3 = (( X1 + X2 ) + 2 ) / float(4)
  B4 = AC4 * ( X3 + 32768 ) / float(32768)
  B7 = (pu - B3) * 50000
  if B7 < 0x80000000:
    p = ( B7 * 2 ) / B4
  else:
    p = ( B7 / float(B4) ) * 2
  X1 = ( p / float(256) ) * ( p / float(256) )
  X1 = ( X1 * 3038 ) / float(25536)
  X2 = (-7357 * p ) / float(25536)
  p = p + (X1 + X2 + 3791) / float(16)

  # print("B6 " + str(B6))
  # print("X1 " + str(X1))
  # print("X2 " + str(X2))
  # print("X3 " + str(X3))
  # print("B3 " + str(B3))
  # print("X1 " + str(X1))
  # print("X2 " + str(X2))
  # print("X3 " + str(X3))
  # print("B4 " + str(B4))
  # print("B7 " + str(B7))
  # print("p " + str(p))
  # print("X1 " + str(X1))
  # print("X1 " + str(X1))
  # print("X2 " + str(X2))


  alt = 44330 * ( 1 - ( p / 101325.0 )**(1/5.255) )

  # print('Temperature: ' + str(T / float(10) ) )
  # print('Pressure: ' + str(p) + 'Pa')
  print("Altitude: " + str(alt) + 'm')
  # print("")

  # sleep(0.5)
