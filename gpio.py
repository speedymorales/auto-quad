#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

while True:
        GPIO.output(16, GPIO.HIGH)
        sleep(.2)
        GPIO.output(16, GPIO.LOW)
        sleep(.2)
        GPIO.output(16, GPIO.HIGH)
        sleep(.2)
        GPIO.output(16, GPIO.LOW)
        sleep(.2)
        GPIO.output(16, GPIO.HIGH)
        sleep(.2)
        GPIO.output(16, GPIO.LOW)
        sleep(1)