#!/usr/bin/env python


##
#  @package weatherStationXml package contains the method to create the xml payload or the weather station
#

import logging
from ModbusConsts import ModbusConsts

class WeatherStationXml:

    LOG = logging.getLogger( __name__ )


    ##
    #
    def createXmlTag( self, key, value ):
        tag = '<' + key + ' V=\'' + str(value) + '\'/>'

        return tag

    ##
    #
    def getXmlPayload( self, decodedData, recordTime ):

        xmlPayload = '<WST id=\'' + decodedData.get( ModbusConsts.DEVICE_ID ) + '\' type=\'' + decodedData.get( ModbusConsts.DEVICE_TYPE ) + '\'>'

        try:
            data = decodedData.get( ModbusConsts.DATA )
            if ModbusConsts.WST_WSNSR in data:
                value = data.get( ModbusConsts.WST_WSNSR )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_WSNSR, value )

            if ModbusConsts.WST_TEMP in data:
                value = data.get( ModbusConsts.WST_TEMP )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_TEMP, value )

            if ModbusConsts.WST_HUMI in data:
                value = data.get( ModbusConsts.WST_HUMI )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_HUMI, value )

            if ModbusConsts.WST_RELAY in data:
                value = data.get( ModbusConsts.WST_RELAY )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_RELAY, value )

            if ModbusConsts.WST_RAIN in data:
                value = data.get( ModbusConsts.WST_RAIN )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_RAIN, value )

            if ModbusConsts.WST_WINDS in data:
                value = data.get( ModbusConsts.WST_WINDS )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_WINDS, value )

            if ModbusConsts.WST_WINDD in data:
                value = data.get( ModbusConsts.WST_WINDD )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_WINDD, value )

            if ModbusConsts.WST_ANLG1 in data:
                value = data.get( ModbusConsts.WST_ANLG1 )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.WST_ANLG1, value )
        except Exception as e:
            pass

        xmlPayload = xmlPayload + '</WST>'

        return xmlPayload
