#!/usr/bin/env python

from ModbusDeviceConfig import ModbusDeviceConfig
from ModbusDeviceList import ModbusDeviceList

config = ModbusDeviceList()

print( config.getModbusDeviceList()[0] )
print( config.getModbusDeviceList()[1] )
