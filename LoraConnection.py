#!/usr/bin/env python

##
#  @package LoraConnection Module contains methods to connect to a serial port
#  on which LORA module is connected with the provided parameters
#  and return an instance of the serial connection
#

import serial
from ModbusConsts import ModbusConsts
import logging

class LoraConnection:

    LOG = logging.getLogger(__name__)

    ## LORA Serial port for communicating with the LORA devices
    SERIAL_PORT = '/dev/ttyS3'

    ##
    #  Function to get the serial connection with the specified connection parameters
    #  @param baudratem int: Baudrate for the connection
    #  @param paritym string: Parity for the connection
    #  @param stopbitsm float: Stopbits for the connection
    #  @param bytesizem int: Byte size for the connection
    #
    #  @return ser Serial connection instance with provided parameters
    #
    def getLoraConnection( self, baudratem, paritym, stopbitsm, bytesizem ):
        if paritym is ModbusConsts.PARITY_NONE:
            paritym = serial.PARITY_NONE
        elif paritym is ModbusConsts.PARITY_EVEN:
            paritym = serial.PARITY_EVEN
        elif paritym is ModbusConsts.PARITY_ODD:
            paritym = serial.PARITY_ODD
        elif paritym is ModbusConsts.PARITY_MARK:
            paritym = serial.PARITY_MARK
        elif paritym is ModbusConsts.PARITY_SPACE:
            paritym = serial.PARITY_SPACE
        else:
            paritym = serial.PARITY_NONE

        if stopbitsm == ModbusConsts.SB_ONE:
            stopbitsm = serial.STOPBITS_ONE
        elif stopbitsm == ModbusConsts.SB_ONE_POINT_FIVE:
            stopbitsm = serial.STOPBITS_ONE_POINT_FIVE
        elif stopbitsm == ModbusConsts.SB_TWO:
            stpbitsm = serial.STOPBITS_TWO
        else:
            stopbitsm = serial.STOPBITS_ONE

        if bytesizem == ModbusConsts.BYTE_FIVE:
            bytesizem = serial.FIVEBITS
        elif bytesizem == ModbusConsts.BYTE_SIX:
            bytesizem = serial.SIXBITS
        elif bytesizem == ModbusConsts.BYTE_SEVEN:
            bytesizem = serial.SEVENBITS
        elif bytesizem == ModbusConsts.BYTE_EIGHT:
            bytesizem = serial.EIGHTBITS
        else:
            bytesizem = serial.EIGHTBITS


        ser = serial.Serial(
            port=self.SERIAL_PORT,
            baudrate = baudratem,
            parity=paritym,
            stopbits=stopbitsm,
            bytesize=bytesizem,
            timeout=1
        )

        return ser
