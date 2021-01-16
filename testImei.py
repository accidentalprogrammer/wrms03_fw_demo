#!/usr/bin/env python

import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.write('AT+CGSN\r\n')
ser.flush()
ser.flushOutput()
time.sleep(1)
size = ser.inWaiting()

data = ser.read(size)
ser.close()
data = data[data.index('\n')+1:]
data = data[:data.index('\n')]
data = data.strip()
print "IMEI:",data
