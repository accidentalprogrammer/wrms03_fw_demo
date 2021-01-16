#!/usr/bin/env python

import logging
from ModbusConsts import ModbusConsts


class SensorXml:

    LOG = logging.getLogger( __name__ )


    ##
    #
    def createXmlTag( self, key, value ):
        tag = '<' + key + ' V=\'' + str(value) + '\'/>'

        return tag

    ##
    #
    def getXmlPayload( self, decodedData, recordTime ):
        xmlPayload = '<SINV id=\'' + decodedData.get( ModbusConsts.DEVICE_ID ) + '\' type=\'' + decodedData.get( ModbusConsts.DEVICE_TYPE ) + '\'>'

        data = decodedData.get( ModbusConsts.DATA )
        print("data in solarxml: ", data)
        if ModbusConsts.SLR_WSNSR in data:
            value = data.get( ModbusConsts.SLR_WSNSR )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_WSNSR, value )

        if ModbusConsts.SLR_TEMP in data:
            value = data.get( ModbusConsts.SLR_TEMP )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_TEMP, value )

        if ModbusConsts.SLR_HUMI in data:
            value = data.get( ModbusConsts.SLR_HUMI )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_HUMI, value )

        if ModbusConsts.SLR_RELAY in data:
            value = data.get( ModbusConsts.SLR_RELAY )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_RELAY, value )

        if ModbusConsts.SLR_RAIN in data:
            value = data.get( ModbusConsts.SLR_RAIN )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_RAIN, value )

        if ModbusConsts.SLR_WINDS in data:
            value = data.get( ModbusConsts.SLR_WINDS )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_WINDS, value )

        if ModbusConsts.SLR_WINDD in data:
            value = data.get( ModbusConsts.SLR_WINDD )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_WINDD, value )

        if ModbusConsts.SLR_ANLG1 in data:
            value = data.get( ModbusConsts.SLR_ANLG1 )
            xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ANLG1, value )

        xmlPayload = xmlPayload + '</SINV>'

        return xmlPayload
