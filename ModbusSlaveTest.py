#!/usr/bin/env python

import serial
import time
import binascii


input = { '140400080001B2CD': '110402000AF8F4', '150400080001B31C': '110402000AF8F4' }

ser = serial.Serial(
    port='/dev/pts/10',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


while True:
    try:
        dataAvailable = ser.inWaiting()
        if dataAvailable > 0:
            data = ser.read( dataAvailable )
            data = ''.join( [ "%02X"%x for x in data ] ).strip()
            print("Received: ",data )
            if data in input:
                print( "Sending: ", input[data] )
                ser.write( bytearray.fromhex( input[data] ) )
                ser.flush()
        else:
            time.sleep( 0.1 )

    except Exception as e:
        print("Exception",e)
