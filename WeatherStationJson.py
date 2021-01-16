#!/usr/bin/env python


##
#  @package weatherStationJson package contains the method to create the JSON payload or the weather station
#

import logging
from ModbusConsts import ModbusConsts

class WeatherStationJson:

    LOG = logging.getLogger( __name__ )



    ##
    #
    def getJsonPayload( self, decodedData, recordTime ):

        jsonPayload = {}
        jsonPayload[ModbusConsts.SLAVE_ID] = decodedData.get( ModbusConsts.SLAVE_ID )
        jsonPayload[ModbusConsts.DEVICE_TYPE] = decodedData.get( ModbusConsts.DEVICE_TYPE )
        jsonPayload[ModbusConsts.DEVICE_CATEGORY] = 'WST'#decodedData.get( ModbusConsts.DEVICE_CATEGORY )
        jsonPayload[ModbusConsts.DEVICE_ID] = decodedData.get( ModbusConsts.DEVICE_ID )
        #jsonData = {}
        try:
            data = decodedData.get( ModbusConsts.DATA )
            if ModbusConsts.WST_WSNSR in data:
                value = data.get( ModbusConsts.WST_WSNSR )
                jsonPayload['module_temp'] = value

            if ModbusConsts.WST_TEMP in data:
                value = data.get( ModbusConsts.WST_TEMP )
                jsonPayload['ambient_temp'] = value

            if ModbusConsts.WST_HUMI in data:
                value = data.get( ModbusConsts.WST_HUMI )
                jsonPayload['humidity'] = value

            if ModbusConsts.WST_RELAY in data:
                value = data.get( ModbusConsts.WST_RELAY )
                jsonPayload['relay'] = value

            if ModbusConsts.WST_RAIN in data:
                value = data.get( ModbusConsts.WST_RAIN )
                jsonPayload['rain'] = value

            if ModbusConsts.WST_WINDS in data:
                value = data.get( ModbusConsts.WST_WINDS )
                jsonPayload['wind_speed'] = value

            if ModbusConsts.WST_WINDD in data:
                value = data.get( ModbusConsts.WST_WINDD )
                jsonPayload['wind_dir'] = value

            if ModbusConsts.WST_ANLG1 in data:
                value = data.get( ModbusConsts.WST_ANLG1 )
                jsonPayload['irradiation'] = value
        except Exception as e:
            self.LOG.error('Error constructing WST json payload: %s', e)

        #jsonPayload[ModbusConsts.DATA] = jsonData

        return jsonPayload

