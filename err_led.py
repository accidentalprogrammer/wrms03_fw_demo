#!/usr/bin/env python 

import OPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BOARD )
GPIO.setup(26, GPIO.OUT)

def toggle_led( time_period ):
    GPIO.output(26, GPIO.HIGH)
    time.sleep(time_period)
    GPIO.output(26, GPIO.LOW)
    time.sleep(time_period)


def led_stable():
    GPIO.output(26, GPIO.LOW)

def led_off():
    GPIO.output(26, GPIO.HIGH)

