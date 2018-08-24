#!/usr/bin/python3

import RPi.GPIO as gpio
from time import sleep

relayPin = 14
gpio.setmode(gpio.BCM)
gpio.setup(relayPin, gpio.OUT)

try:
    gpio.output(relayPin, 0)
    while True:
        gpio.output(relayPin, 1)
        sleep(0.5)
        gpio.output(relayPin, 0)
        sleep(6.0)

    gpio.output(relayPin, 0)
except KeyboardInterrupt:
    gpio.cleanup()
