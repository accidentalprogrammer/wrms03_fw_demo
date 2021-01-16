#!/usr/bin/env python

##
#  @package ModbusCommandSender Module contains the logic to send Modbus commands
#

from SerialConnection import SerialConnection
from ModbusConsts import ModbusConsts
import ModbusLib
import logging
import time
import Status
import OPi.GPIO as GPIO

class ModbusCommandSender:
    LOG = logging.getLogger(__name__)

    ##
    #  Function to query the all the register sets for the device and return the data
    #  @param slaveId int: Slave ID of the controller
    #  @param ser Serial: Serial connection to communicate with the device
    #  @param regSetList List: List of the register sets to be queried
    #
    #  @return response dictionary: Dictionary containig the response of the each register set query with key as 'funId'_'startReg'
    #
    def sendCommand( self, ser, command, connType=None ):
        if ser is None:
            return False
        response = False
        time.sleep(0.5)
        respByteCount = 4
        expectedResp = command[:8]
        message = bytearray.fromex( command )
        if connType == ModbusConsts.CONN_RTU:
            respByteCount += 0 # Receiving one extra byte in the begining
        retries = 7
        data = None
        while( retries > 0 ):
            retries -= 1
            ser.flushInput()
            if connType == ModbusConsts.CONN_RTU:
                GPIO.output(15,1) #set high/transmit
            time.sleep(0.1)
            ser.write( message )
            time.sleep(0.008)
            ser.flushOutput()
            if connType == ModbusConsts.CONN_RTU:
                GPIO.output(15,0) #set low/receive
            time.sleep(0.01)
            timeout = 2000
            size = 0
            while( timeout > 0 ):
                size = ser.inWaiting()
                if size >= respByteCount:
                    break
                else:
                    timeout = timeout - 10
                    time.sleep( 0.01 )
            time.sleep(0.5)
            size = ser.inWaiting()
            if size >= respByteCount:
                print('expected size: ', respByteCount)
                print('received', size)
                data = ser.read( size )
                dataStr = ''.join( [ "%02X"%x for x in data ] ).strip()
                print(dataStr)
                startIdx = dataStr.find(expectedResp)
                if startIdx >= 0:
                  response = True
                  retries = 0
        ser.close()
        return response

