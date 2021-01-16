#!/usr/bin/env python

import OPi.GPIO as GPIO
import time

# Pin Definitons:
onPin = 16 
pwrKey = 12
statusPin = 18


#GPIO.setboard(GPIO.ZERO)
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(onPin, GPIO.OUT) 
GPIO.setup(pwrKey, GPIO.OUT)
GPIO.setup(statusPin, GPIO.IN)


if GPIO.input(statusPin) == 1: # If status pin is high 
    # Toggle the Power Key
    GPIO.output(pwrKey, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(pwrKey, GPIO.LOW)
    time.sleep(30)

    print('GSM Status: ', GPIO.input(statusPin))
else: # If status pin is not High
    GPIO.output(onPin, GPIO.HIGH) # set the GSM ON/OFF pin to high
    time.sleep(5)
    # Then Toggle the power key
    GPIO.output(pwrKey, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(pwrKey, GPIO.LOW)
    time.sleep(30)
    print('GSM Status: ', GPIO.input(statusPin))

