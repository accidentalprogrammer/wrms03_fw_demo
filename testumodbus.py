#!/usr/bin/env python
# scripts/example/simple_rtu_client.py


import ModbusLib

message = ModbusLib.readInputRegisterRtu( 20, 180, 100 )
print ( message )
