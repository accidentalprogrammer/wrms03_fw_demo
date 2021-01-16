#!/usr/bin/env python


import logging
from ModbusConsts import ModbusConsts

class AbbInverter100Xml:
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
        try:
            data = decodedData.get( ModbusConsts.DATA )
            if '1WSNSR' in data:
                value = data.get( '1WSNSR' )
                xmlPayload = xmlPayload + self.createXmlTag( '1WSNSR', value )

            if 'TEMP' in data:
                value = data.get( 'TEMP' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TEMP', value )

            if 'HUMI' in data:
                value = data.get( 'HUMI' )
                xmlPayload = xmlPayload + self.createXmlTag( 'HUMI', value )

            if 'RELAY' in data:
                value = data.get( 'RELAY' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RELAY', value )

            if 'RAIN' in data:
                value = data.get( 'RAIN' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RAIN', value )

            if 'WINDS' in data:
                value = data.get( 'WINDS' )
                xmlPayload = xmlPayload + self.createXmlTag( 'WINDS', value )

            if 'WINDD' in data:
                value = data.get( 'WINDD' )
                xmlPayload = xmlPayload + self.createXmlTag( 'WINDD', value )

            if 'ANLG1' in data:
                value = data.get( 'ANLG1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'ANLG1', value )

            if 'Amp_All' in data:
                value = data.get( 'Amp_All' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Amp_All', value )

            if 'Amp_A' in data:
                value = data.get( 'Amp_A' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Amp_A', value )

            if 'Amp_B' in data:
                value = data.get( 'Amp_B' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Amp_B', value )

            if 'Amp_c' in data:
                value = data.get( 'Amp_c' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Amp_c', value )

            if 'Amp_Sf' in data:
                value = data.get( 'Amp_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Amp_Sf', value )

            if 'Volt_A' in data:
                value = data.get( 'Volt_A' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_A', value )

            if 'Volt_B' in data:
                value = data.get( 'Volt_B' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_B', value )

            if 'Volt_C' in data:
                value = data.get( 'Volt_C' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_C', value )

            if 'Volt_AN' in data:
                value = data.get( 'Volt_AN' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_AN', value )

            if 'Volt_BN' in data:
                value = data.get( 'Volt_BN' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_BN', value )

            if 'Volt_CN' in data:
                value = data.get( 'Volt_CN' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_CN', value )

            if 'Volt_Sf' in data:
                value = data.get( 'Volt_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Volt_Sf', value )

            if 'Watt' in data:
                value = data.get( 'Watt' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Watt', value )

            if 'Watt_Sf' in data:
                value = data.get( 'Watt_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Watt_Sf', value )

            if 'Hz' in data:
                value = data.get( 'Hz' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Hz', value )

            if 'Hz_Sf' in data:
                value = data.get( 'Hz_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Hz_Sf', value )

            if 'VA' in data:
                value = data.get( 'VA' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VA', value )

            if 'VA_Sf' in data:
                value = data.get( 'VA_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VA_Sf', value )

            if 'VAr' in data:
                value = data.get( 'VAr' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VAr', value )

            if 'VAr_Sf' in data:
                value = data.get( 'VAr_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VAr_Sf', value )

            if 'PF' in data:
                value = data.get( 'PF' )
                xmlPayload = xmlPayload + self.createXmlTag( 'PF', value )

            if 'PF_Sf' in data:
                value = data.get( 'PF_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'PF_Sf', value )

            if 'WattH' in data:
                value = data.get( 'WattH' )
                xmlPayload = xmlPayload + self.createXmlTag( 'WattH', value )

            if 'WattH_Sf' in data:
                value = data.get( 'WattH_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'WattH_Sf', value )

            if 'DCA' in data:
                value = data.get( 'DCA' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCA', value )

            if 'DCA_Sf' in data:
                value = data.get( 'DCA_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCA_Sf', value )

            if 'DCV' in data:
                value = data.get( 'DCV' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCV', value )

            if 'DCV_Sf' in data:
                value = data.get( 'DCV_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCV_Sf', value )

            if 'DCW' in data:
                value = data.get( 'DCW' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCW', value )

            if 'DCW_Sf' in data:
                value = data.get( 'DCW_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCW_Sf', value )

            if 'TempCab' in data:
                value = data.get( 'TempCab' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TempCab', value )

            if 'TempSink' in data:
                value = data.get( 'TempSink' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TempSink', value )

            if 'TempTrans' in data:
                value = data.get( 'TempTrans' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TempTrans', value )

            if 'TempOthr' in data:
                value = data.get( 'TempOthr' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TempOthr', value )

            if 'Temp_Sf' in data:
                value = data.get( 'Temp_Sf' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Temp_Sf', value )

            if 'Op_State' in data:
                value = data.get( 'Op_State' )
                xmlPayload = xmlPayload + self.createXmlTag( 'Op_State', value )
        except Exception as e:
            self.LOG.debug( 'Error constructing Abb 100 KW payload: %s', e )


        xmlPayload = xmlPayload + '</SINV>'

        return xmlPayload
