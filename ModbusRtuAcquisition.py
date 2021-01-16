#!/usr/bin/env python

##
#  @package ModbusRtuAcquisition Module contains the logic to query the Modbus RTU devices
#

from SerialConnection import SerialConnection
from ModbusConsts import ModbusConsts
import ModbusLib
import logging
import time
import Status
import OPi.GPIO as GPIO

class ModbusRtuAcquisition:
    LOG = logging.getLogger(__name__)


    ##
    #  Function to get the Modbus command in the RTU format
    #  @param slaveId int: slave ID of the controller
    #  @param funId int: function ID of the request
    #  @param startReg int: Starting register for the query
    #  @param regCount int: Number of registers o be queried
    def getModbusRtuMessage( self, slaveId, funId, startReg, regCount ):
        if funId == 1:
            message = ModbusLib.readDiscreteCoilsRtu( slaveId, startReg, regCount )
        elif funId == 2:
            message = ModbusLib.readDiscreteInputRtu( slaveId, startReg, regCount )
        elif funId == 3:
            message = ModbusLib.readHoldingRegisterRtu( slaveId, startReg, regCount )
        elif funId == 4:
            message = ModbusLib.readInputRegisterRtu( slaveId, startReg, regCount )
        else:
            message = None

        return message


    ##
    #  Function to get the number of bytes to be received in response of the modbus request
    #  @param funId int: Function ID of the request
    #  @param regCount int: Number of registers queried
    #
    def getNumberOfResposeBytes( self, funId, regCount ):
        byteCount = 0

        if funId == 1 or funId == 2:
            padding = 0 if (regCount % 8) == 0 else 8 - (regCount % 8)
            if padding == 0:
                byteCount = 3 + (regCount / 8) + 2
            else:
                byteCount = 3 + ( regCount / 8 ) +1 + 3
        elif funId == 3 or funId == 4:
            byteCount = 3 + (regCount * 2) + 2

        return byteCount


    ##
    #  Function to query the all the register sets for the device and return the data
    #  @param slaveId int: Slave ID of the controller
    #  @param ser Serial: Serial connection to communicate with the device
    #  @param regSetList List: List of the register sets to be queried
    #
    #  @return response dictionary: Dictionary containig the response of the each register set query with key as 'funId'_'startReg'
    #
    def queryDevice( self, slaveId, ser, regSetList, devIndex, connType=None ):
        if ser is None:
            Status.modbusDevStatus[devIndex] += 1
            return {}
        self.LOG.debug(regSetList)
        response = {}
        for regSet in regSetList:
            time.sleep(0.5)
            self.LOG.debug( 'Querying: %s', regSet )
            funId = int(regSet.get( ModbusConsts.FUNCTION_ID ))
            startReg = int(regSet.get( ModbusConsts.START_REG ))
            regCount = int(regSet.get( ModbusConsts.REG_COUNT ))
            message = self.getModbusRtuMessage( slaveId, funId, startReg, regCount )
            strLookupBytes = message[0:2]
            strLookup = ''.join( [ "%02X"%x for x in strLookupBytes ] ).strip()
            respByteCount = self.getNumberOfResposeBytes( funId, regCount )
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
                if size == respByteCount:
                    print('expected size: ', respByteCount)
                    print(size)
                    data = ser.read( respByteCount )
                    dataStr = ''.join( [ "%02X"%x for x in data ] ).strip()
                    print(dataStr)
                    print('Received: ',data)
                    if dataStr.find(strLookup) == 0:
                        retries = 0
                elif size >= respByteCount:
                    print('expected size: ', respByteCount)
                    print('received', size)
                    data = ser.read( size )
                    dataStr = ''.join( [ "%02X"%x for x in data ] ).strip()
                    print(dataStr)
                    startIdx = dataStr.find(strLookup)
                    try:
                        if startIdx >= 0 and (startIdx+respByteCount) <= size:
                            dataStr = dataStr[startIdx:(startIdx+(respByteCount*2))]
                            print(dataStr)
                            data = bytes.fromhex(dataStr)
                            retries = 0
                    except Exception as e2:
                        self.LOG.error('Error extracting modbus data %s', e)
                else:
                    print('expected size: ', respByteCount)
                    print(size)
                    self.LOG.warning( 'No data received for the modbus query.' )
                    data = None

                if data is not None:
                    crc = data[-2:]  # Take out the CRC
                    crc = ''.join( [ "%02X"%x for x in crc ] ).strip()
                    data = data[:-2] # Strip out the CRC from the data
                    crcCalc = ModbusLib.get_modbus_crc( data )  # TODO: implement Dynamic function invocation for calculation of CRC
                    if crcCalc != crc:
                        self.LOG.warning( 'CRC does not match for the received data. Data will be discarded' )
                        data = None

                if data is None:
                    Status.modbusDevStatus[devIndex] += 1
                else:
                    Status.modbusDevStatus[devIndex] = 0
                    dataKey = "%02X"%funId +"_"+ "%04X"%startReg
                    response[dataKey] = data[3:]
        ser.close()
        return response

