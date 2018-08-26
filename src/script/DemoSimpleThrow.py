#!/usr/bin/python3

import RPi.GPIO as gpio
from time import sleep
from GpioPinHandler import GpioPinHandler


pinHandler = GpioPinHandler()
outPin = pinHandler.registerOutPin(14)

try:
    outPin.setLow()
    while True:
        outPin.setHigh()
        sleep(0.5)
        outPin.setLow()
        sleep(6.0)

finally:
    outPin.setLow()
    gpio.cleanup()
