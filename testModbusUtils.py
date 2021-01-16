#!/usr/bin/env python

import ModbusUtils

hexstr = '5AA5'
print( int( hexstr, 16 ) )

barr = bytearray.fromhex(hexstr)
print(barr)
print(ModbusUtils.bytesToInt(barr))
