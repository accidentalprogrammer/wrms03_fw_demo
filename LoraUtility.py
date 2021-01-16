#!/usr/bin/env python

##
#  @package LoraUtility Package contains the miscelaneous functions for the LORA Module
#


from LoraConnection import LoraConnection
from ModbusConsts import ModbusConsts
import time

##
#  Function to change the LORA communication channel
#  @param channel int: new channel no to be set for the LORA communication
#  @return result boolean: Returns True if the channel was changed successfully False otherwise
def setChannel( channel ):
    checkConfigCmd = "C1C1C1"
    ser = LoraConnection().getLoraConnection( 9600, ModbusConsts.PARITY_NONE, ModbusConsts.SB_ONE, ModbusConsts.BYTE_EIGHT )
    if ser == None:
        return False

    ser.flushInput()
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
        print(''.join('{:02x}'.format(x) for x in data))
        currentChannel = int( data[4] )

    ser.flushInput()
    channelChangeCmd = "C000001A" + "%02X"%channel + "44"
    ser.write( bytearray.fromhex(channelChangeCmd) )
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
        print(''.join('{:02x}'.format(x) for x in data))
        currentChannel = int( data[4] )
        if currentChannel == channel:
            return True

    return False
