#!/usr/bin/env python


from MessageComposer import MessageComposer
import PeriodicTimer
from ModbusConsts import ModbusConsts
import InputDataQueue
import simplejson as json
import time

pt = PeriodicTimer.PeriodicTimer().start()
time.sleep(1)
print(PeriodicTimer.counter)
time.sleep(PeriodicTimer.counter)
#Messagecomposer().start()

tcs_data = {}
tcs_data[ModbusConsts.TCS_SERVICE] = 'kSOS'
tcs_data[ModbusConsts.TCS_VERSION] = '2.0'
tcs_data[ModbusConsts.TCS_OBS_FEATURE] = 'Pune-Demo-Farm'
tcs_data[ModbusConsts.TCS_OBS_SENSOR] = 'SP-Pune-WB-Gateway'
tcs_data[ModbusConsts.TCS_GEO_TYPE] = 'Point'
tcs_data[ModbusConsts.TCS_COORD_ALTITUDE] = 560.0
tcs_data[ModbusConsts.TCS_COORD_LATITUDE] = 73.680639
tcs_data[ModbusConsts.TCS_COORD_LONGITUDE] = 18.580211

modbusRespList = []
data = {'Ambient Temperature': '26.0'}
modbusResp = { 'tcs_data': tcs_data, 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)


data = {'Relative Humidity': '66.0'}
modbusResp = { 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)

data = {'Rain Gauge': '5.0'}
modbusResp = { 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)

data = {'Leaf Wetness': '16.0'}
modbusResp = { 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)

data = {'Leaf Temp': '23.0'}
modbusResp = { 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)

data = {'Wind Speed': '275.0'}
modbusResp = { 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)

data = {'Wind Direction': '40.5'}
modbusResp = { 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Gateway_Offering' }
modbusRespList.append(modbusResp)

tcs_data2 = {}
tcs_data2[ModbusConsts.TCS_SERVICE] = 'kSOS'
tcs_data2[ModbusConsts.TCS_VERSION] = '2.0'
tcs_data2[ModbusConsts.TCS_OBS_FEATURE] = 'Pune-Demo-Farm'
tcs_data2[ModbusConsts.TCS_OBS_SENSOR] = 'SP-Pune-WB-Gateway'
tcs_data2[ModbusConsts.TCS_GEO_TYPE] = 'Point'
tcs_data2[ModbusConsts.TCS_COORD_ALTITUDE] = 560.0
tcs_data2[ModbusConsts.TCS_COORD_LATITUDE] = 73.680639
tcs_data2[ModbusConsts.TCS_COORD_LONGITUDE] = 18.580211


tcs_data2[ModbusConsts.TCS_OBS_SENSOR] = 'SP-Pune-WB-Node1'
data = {}
data = {'soil moisture': 76.0, 'soil temperature':26.0, 'soil electrical conductivity':11.0}
modbusResp = { 'tcs_data': tcs_data2, 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Node1_Offering' }
modbusRespList.append(modbusResp)

tcs_data3 = {}
tcs_data3[ModbusConsts.TCS_SERVICE] = 'kSOS'
tcs_data3[ModbusConsts.TCS_VERSION] = '2.0'
tcs_data3[ModbusConsts.TCS_OBS_FEATURE] = 'Pune-Demo-Farm'
tcs_data3[ModbusConsts.TCS_OBS_SENSOR] = 'SP-Pune-WB-Gateway'
tcs_data3[ModbusConsts.TCS_GEO_TYPE] = 'Point'
tcs_data3[ModbusConsts.TCS_COORD_ALTITUDE] = 560.0
tcs_data3[ModbusConsts.TCS_COORD_LATITUDE] = 73.680639
tcs_data3[ModbusConsts.TCS_COORD_LONGITUDE] = 18.580211


tcs_data3[ModbusConsts.TCS_OBS_SENSOR] = 'SP-Pune-WB-Node2'
data = {}
data = {'soil moisture': 76.0, 'soil temperature':26.0, 'soil electrical conductivity': 11.0}
modbusResp = { 'tcs_data': tcs_data3, 'data':data, ModbusConsts.TCS_OFFERING:'SP-Pune-WB-Node2_Offering' }
modbusRespList.append(modbusResp)


InputDataQueue.modbusDataQueue.put_nowait( modbusRespList )

mc = MessageComposer()
print(json.dumps(mc.constructTcsPayload()))


