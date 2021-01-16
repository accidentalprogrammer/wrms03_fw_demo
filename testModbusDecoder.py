#!/usr/bin/env python


from ModbusDecoder import ModbusDecoder


mdec = ModbusDecoder()

hexstr = '437a0000'
barr = bytearray.fromhex( hexstr )
print(barr)
mresponse = { 'device_type': 'sample_config', 'slave_id': 10, '04_0064': barr}
respList = [mresponse]

param = { 'name': 'IntValue', 'register_size': 16, 'param_size': 32, 'type': 'SwappedFloat16', 'byte_offset': 0, 'bit_offset': 0, 'sign': 'U', 'formula': '($this*0.01)' }

decoded = {}

decoded = mdec.decodeModbusData( respList )
print(decoded)
