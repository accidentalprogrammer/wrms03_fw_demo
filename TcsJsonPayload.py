#!/usr/bin/env python


##
#  @package TcsJsonPayload package contains the functions to construct the JSON payload for the different devices
#

import logging
from ModbusConsts import ModbusConsts

class TcsJsonPayload:

    LOG = logging.getLogger( __name__ )

    ##
    #
    def constructPayload( self, modbusRespList, recordTime ):
        if modbusRespList is None:
            return {}

        payload_dict = {}
        for modbusResp in modbusRespList:
            payload = {}
            group = modbusResp.get( ModbusConsts.TCS_OFFERING )
            if group in payload_dict:
                payload = payload_dict.get( group )
            payload['offering'] = group
            observation = {}
            if 'observation' in payload:
                observation = payload['observation']
            if ModbusConsts.TCS_DATA in modbusResp:
                tcsData = modbusResp.get( ModbusConsts.TCS_DATA )
                payload['request'] = 'InsertObservation'
                payload['service'] = tcsData.get( ModbusConsts.TCS_SERVICE )
                payload['version'] = tcsData.get( ModbusConsts.TCS_VERSION )
                coordinates = [ tcsData.get( ModbusConsts.TCS_COORD_ALTITUDE ), tcsData.get( ModbusConsts.TCS_COORD_LATITUDE ), tcsData.get( ModbusConsts.TCS_COORD_LONGITUDE ) ]
                geometry = {}
                geometry['type'] = tcsData.get( ModbusConsts.TCS_GEO_TYPE )
                geometry['coordinates'] = coordinates
                observation['sensor'] = tcsData.get( ModbusConsts.TCS_OBS_SENSOR )
                observation['feature'] = tcsData.get( ModbusConsts.TCS_OBS_FEATURE )
                observation['geometry'] = geometry
                observation['phenomenonTime'] = recordTime
                observation['resultTime'] = recordTime
                payload['observation'] = observation

            data = []
            if 'output' in payload:
                data = payload.get( 'output' )

            data = self.constructData( data, modbusResp.get(ModbusConsts.DATA) )
            observation = payload['observation']
            observation['output'] = data
            payload['observation'] = observation
            payload_dict[group] = payload

        payloadList = []
        for key,val in payload_dict.items():
            payloadList.append(val)

        return payloadList


    ##
    #
    def constructData( self, outputData, inputData ):
        if 'Ambient Temperature' in inputData:
            value = inputData.get( 'Ambient Temperature' )
            paramData = {}
            paramData['property'] = 'Ambient Temperature'
            paramData['type'] = 'double'
            paramData['unit'] = '°C'
            paramData['value'] = value
            outputData.append(paramData)

        if 'Relative Humidity' in inputData:
            value = inputData.get( 'Relative Humidity' )
            paramData = {}
            paramData['property'] = 'Relative Humidity'
            paramData['type'] = 'double'
            paramData['unit'] = '%'
            paramData['value'] = value
            outputData.append(paramData)

        if 'Rain Gauge' in inputData:
            value = inputData.get( 'Rain Gauge' )
            paramData = {}
            paramData['property'] = 'Rain Gauge'
            paramData['type'] = 'double'
            paramData['unit'] = 'mm'
            paramData['value'] = value
            outputData.append(paramData)

        if 'Leaf Wetness' in inputData:
            value = inputData.get( 'Leaf Wetness' )
            paramData = {}
            paramData['property'] = 'Leaf Wetness'
            paramData['type'] = 'double'
            paramData['unit'] = '%'
            paramData['value'] = value
            outputData.append(paramData)

        if 'Leaf Temp' in inputData:
            value = inputData.get( 'Leaf Temp' )
            paramData = {}
            paramData['property'] = 'Leaf Temp'
            paramData['type'] = 'double'
            paramData['unit'] = '°C'
            paramData['value'] = value
            outputData.append(paramData)

        if 'Wind Speed' in inputData:
            value = inputData.get( 'Wind Speed' )
            paramData = {}
            paramData['property'] = 'Wind Speed'
            paramData['type'] = 'double'
            paramData['unit'] = 'm/sec'
            paramData['value'] = value
            outputData.append(paramData)

        if 'Wind Direction' in inputData:
            value = inputData.get( 'Wind Direction' )
            paramData = {}
            paramData['property'] = 'Wind Direction'
            paramData['type'] = 'double'
            paramData['unit'] = 'degree ( °)'
            paramData['value'] = value
            outputData.append(paramData)

        if 'soil moisture' in inputData:
            value = inputData.get( 'soil moisture' )
            paramData = {}
            paramData['property'] = 'soil moisture'
            paramData['type'] = 'double'
            paramData['unit'] = '%'
            paramData['value'] = value
            outputData.append(paramData)

        if 'soil temperature' in inputData:
            value = inputData.get( 'soil temperature' )
            paramData = {}
            paramData['property'] = 'soil temperature'
            paramData['type'] = 'double'
            paramData['unit'] = '°C'
            paramData['value'] = value
            outputData.append(paramData)

        if 'soil electrical conductivity' in inputData:
            value = inputData.get( 'soil electrical conductivity' )
            paramData = {}
            paramData['property'] = 'soil electrical conductivity'
            paramData['type'] = 'double'
            paramData['unit'] = 'dS/m'
            paramData['value'] = value
            outputData.append(paramData)

        return outputData


