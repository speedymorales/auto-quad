#!/usr/bin/python

import smbus
from time import sleep

bus = smbus.SMBus(1)

# LSM303D - 3 axis accelerometer, 3 axis magnetometer
DEVICE_ADDRESS = 0x1D

CTRL_REG0 = 0x1F
CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0x24
CTRL_REG6 = 0x25
CTRL_REG7 = 0x26

# REFERENCE = 0x25
# STATUS_REG = 0x27
MAG_STATUS_REG = 0x07
ACC_STATUS_REG = 0x27

MAG_OFFSET_X_REG = 0x16
MAG_OFFSET_Y_REG = 0x18
MAG_OFFSET_Z_REG = 0x20
# FIFO_CTRL_REG = 0x2E
# FIFO_SRC_REG = 0x2F
# INT1_CFG = 0x30
# INT1_SRC = 0x31
# INT1_THS_XH = 0x32
# INT1_THS_XL = 0x33
# INT1_THS_YH = 0x34
# INT1_THS_YL = 0x35
# INT1_THS_ZH = 0x36
# INT1_THS_ZL = 0x37
# INT_DURATION = 0x38


OUT_TEMP_12 = 0x05

MAG_OUT_X_16 = 0x08
MAG_OUT_Y_16 = 0x0A
MAG_OUT_Z_16 = 0x0C

ACC_OUT_X_16 = 0x28
ACC_OUT_Y_16 = 0x2A
ACC_OUT_Z_16 = 0x2C

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
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG0, 0b00000000)
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG1, 0b01100111) # 100Hz Acc, Enable x,y,z
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG2, 0b00000000)
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG3, 0b00000000)
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG4, 0b00000000)
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG5, 0b00010100) # 100Hz Mag
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG6, 0b01000000) # Mag +/- 8 gauss
  bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG7, 0b00000000) # Mag continuous conversion

init()

while True:
  sleep(0.02)
  # sleep(1)

  mag_status = bus.read_byte_data(DEVICE_ADDRESS, MAG_STATUS_REG)
  # print("{0:b}".format(status))

  while mag_status & 0x07 != 0x07:
    mag_status = bus.read_byte_data(DEVICE_ADDRESS, MAG_STATUS_REG)

  mag_x = signedWord(readWord(DEVICE_ADDRESS, MAG_OUT_X_16))
  mag_y = signedWord(readWord(DEVICE_ADDRESS, MAG_OUT_Y_16))
  mag_z = signedWord(readWord(DEVICE_ADDRESS, MAG_OUT_Z_16))

  acc_status = bus.read_byte_data(DEVICE_ADDRESS, MAG_STATUS_REG)
  # print("{0:b}".format(status))

  while acc_status & 0x07 != 0x07:
    acc_status = bus.read_byte_data(DEVICE_ADDRESS, ACC_STATUS_REG)

  acc_x = signedWord(readWord(DEVICE_ADDRESS, ACC_OUT_X_16))
  acc_y = signedWord(readWord(DEVICE_ADDRESS, ACC_OUT_Y_16))
  acc_z = signedWord(readWord(DEVICE_ADDRESS, ACC_OUT_Z_16))

  print('Mag - X: ' + str(mag_x) + ' Y: ' + str(mag_y) + ' Z: ' + str(mag_z))
  print('Acc - X: ' + str(acc_x) + ' Y: ' + str(acc_y) + ' Z: ' + str(acc_z))
  print("")
  