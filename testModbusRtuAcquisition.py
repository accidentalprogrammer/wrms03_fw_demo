#!/usr/bin/env python


from ModbusDataService import ModbusDataService

mServiceThread = ModbusDataService()
mServiceThread.queryModbusDevices()
