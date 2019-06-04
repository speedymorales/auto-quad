#!/usr/bin/python

import smbus
from time import sleep

bus = smbus.SMBus(1)

# L3GD20 - 3 axis gyro
DEVICE_ADDRESS = 0x6B

CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0x24
REFERENCE = 0x25
STATUS_REG = 0x27
FIFO_CTRL_REG = 0x2E
FIFO_SRC_REG = 0x2F
INT1_CFG = 0x30
INT1_SRC = 0x31
INT1_THS_XH = 0x32
INT1_THS_XL = 0x33
INT1_THS_YH = 0x34
INT1_THS_YL = 0x35
INT1_THS_ZH = 0x36
INT1_THS_ZL = 0x37
INT_DURATION = 0x38

OUT_TEMP = 0x26
OUT_X_16 = 0x28
OUT_Y_16 = 0x2A
OUT_Z_16 = 0x2C

def readWord(addr, cmd):
  # dSet = bus.read_i2c_block_data(addr, cmd)
  dSet0 = bus.read_byte_data(addr, cmd)
  dSet1 = bus.read_byte_data(addr, cmd + 1)

  return dSet1 << 8 | dSet0

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
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG1, 0x0F) # Powerdown High (off), XYZ Enabled
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG2, 0x00) # High pass mode: normal, Cut-Off Freq: 7.2 Hz
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG3, 0x00)
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG4, 0x10) # Block data update: complete, BLE: LSB, Scale: 00 - 250, 01 - 500, 11 - 2000 dps
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG5, 0x00) # FIFO disabled, High Pass Disabled

init()

while True:
  # sleep(0.02)
  sleep(1)

  status = bus.read_byte_data(DEVICE_ADDRESS, STATUS_REG)
  # print("{0:b}".format(status))

  while status & 0x07 != 0x07:
    # sleep(0.005)
    status = bus.read_byte_data(DEVICE_ADDRESS, STATUS_REG)
  dX = signedWord(readWord(DEVICE_ADDRESS, OUT_X_16))
  dY = signedWord(readWord(DEVICE_ADDRESS, OUT_Y_16))
  dZ = signedWord(readWord(DEVICE_ADDRESS, OUT_Z_16))

  print('X: ' + str(dX) + ' Y: ' + str(dY) + ' Z: ' + str(dZ))
  print("")
  