#!/usr/bin/env python

import time
import OPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BOARD)

GPIO.setup(22, GPIO.OUT)
GPIO.output(22,1) # Turn on the LoRa Module
time.sleep(5)   # Wait for some time to turn it on

#GPIO.setup(15, GPIO.OUT)
#GPIO.output(8,1)    # Put the LoRa module in config mode
time.sleep(2)


def setChannel( channel ):
    ser = serial.Serial(
        port='/dev/ttyS3',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

    checkConfigCmd = "C1C1C1"
    if ser == None:
        return False

    ser.flushInput()
    time.sleep(0.1)
    ser.write( bytearray.fromhex( checkConfigCmd ) )
    time.sleep(0.008)
    ser.flushOutput()
    timeout = 5000
    size = 0
    data = None
    while( timeout > 0 ):
        size = ser.inWaiting()
        if size == 6:
            break
        else:
            timeout = timeout - 10
            time.sleep( 0.01 )
    print(size)
    if size == 6:
        data = ser.read( size )
        print(data)
        currentChannel = int( data[8:10], 16 )
        if currentChannel == channel:
            return True
    print(data)
    ser.flushInput()
    channelChangeCmd = "C000001A" + "%02X"%channel + "44"
    ser.write( bytearray.fromhex(channelChangeCmd) )
    time.sleep(0.1)
    ser.flushOutput()

    timeout = 5000
    size = 0
    data = None
    while( timeout > 0 ):
        size = ser.inWaiting()
        if size == 6:
            break
        else:
            timeout = timeout - 10
            time.sleep( 0.01 )
    print(size)
    if size == 6:
        data = ser.read( size )
        currentChannel = int( data[8:10], 16 )
        if currentChannel == channel:
            return True
    print(data)
    return False


setChannel(8) # set the channel
