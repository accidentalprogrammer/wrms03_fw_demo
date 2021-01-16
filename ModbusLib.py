#!/usr/bin/env python


##
#  @package ModbusLib Module containing all the modbus message construction related functions
#



##
#  Function to get the Modbus CRC of the data provided
#  @param data bytearray: data for which the CRC needs to be calculated
#
#  @return crcs string: Modbus CRC of the given data in hex string format
#
def get_modbus_crc( data ):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    crcs = "%04X"%(crc)
    crcs = crcs[2:] + crcs[0:2]
    return crcs


##
#  Function to construct the Modbus message for in the RTU format
#  @param slaveId int: slaveId of the controller to be queried
#  @param funId int: function ID of the request
#  @param startReg int: Starting register of the register set to be queried
#  @param regCount int: Number of registers to be queried
#
#  @return message string: Message to be sent to the controller in the format of hexadecimal string
def _constructRtuReadCommand( slaveId, funId, startReg, regCount ):
    slaveIdHex = "%02X"%slaveId
    funIdHex = "%02X"%funId
    startRegHex = "%04X"%startReg
    regCountHex = "%04X"%regCount
    message = slaveIdHex + funIdHex + startRegHex + regCountHex
    crc = get_modbus_crc( bytearray.fromhex( message ) )
    message = message+crc
    print( message )
    return message



##
#  Function to create the Modbus RTU message to read discrete coils
#  @param slaveId int: slave ID of the controller to be queried
#  @param startCoil int: Starting coil of the set to be queried
#  @param coilCount int: Number of coils to be queried
#
#  @return message bytearray: message to be sent to the Modbus controller to read holding register
#
def readDiscreteCoilsRtu( slaveId, startCoil, coilCount ):
    funId = 1
    message = _constructRtuReadCommand( slaveId, funId, startCoil, coilCount )
    return bytearray.fromhex( message )

##
#  Function to create the Modbus RTU message to read discrete inputs
#  @param slaveId int: slave ID of the controller to be queried
#  @param startReg int: Starting register of the register set to be queried
#  @param regCount int: Number of registers to be queried
#
#  @return message bytearray: message to be sent to the Modbus controller to read holding register
#
def readDiscreteInputRtu( slaveId, startReg, regCount ):
    funId = 2
    message = _constructRtuReadCommand( slaveId, funId, startReg, regCount )
    return bytearray.fromhex( message )

##
#  Function to create the Modbus RTU message to read holding register
#  @param slaveId int: slave ID of the controller to be queried
#  @param startReg int: Starting register of the register set to be queried
#  @param regCount int: Number of registers to be queried
#
#  @return message bytearray: message to be sent to the Modbus controller to read holding register
#
def readHoldingRegisterRtu( slaveId, startReg, regCount ):
    funId = 3
    message = _constructRtuReadCommand( slaveId, funId, startReg, regCount )
    return bytearray.fromhex( message )

##
#  Function to create the Modbus RTU message to read input register
#  @param slaveId int: slave ID of the controller to be queried
#  @param startReg int: Starting register of the register set to be queried
#  @param regCount int: Number of registers to be queried
#
#  @return message bytearray: message to be sent to the Modbus controller to read holding register
#
def readInputRegisterRtu( slaveId, startReg, regCount ):
    funId = 4
    message = _constructRtuReadCommand( slaveId, funId, startReg, regCount )
    return bytearray.fromhex( message )

# TODO: Implement TCP command construction

##
#
def _constructTcpReadCommand( slaveId, funId, startReg, regCount ):
    pass
