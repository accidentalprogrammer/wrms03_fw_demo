#!/usr/bin/env python


##
#  @package SolarInverterXml Package contains the method to create the xml payload for the solar inverter
#

import logging
from ModbusConsts import ModbusConsts

class SolarInverterXml:

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

            if ModbusConsts.SLR_IPPWR in data:
                value = data.get( ModbusConsts.SLR_IPPWR )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_IPPWR, value )

            if ModbusConsts.SLR_OPPWR in data:
                value = data.get( ModbusConsts.SLR_OPPWR )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_OPPWR, value )

            if ModbusConsts.SLR_APP in data:
                value = data.get( ModbusConsts.SLR_APP )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_APP, value )

            if ModbusConsts.SLR_APP1 in data:
                value = data.get( ModbusConsts.SLR_APP1 )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_APP1, value )

            if ModbusConsts.SLR_APP2 in data:
                value = data.get( ModbusConsts.SLR_APP2 )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_APP2, value )

            if ModbusConsts.SLR_APP3 in data:
                value = data.get( ModbusConsts.SLR_APP3 )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_APP3, value )

            if ModbusConsts.SLR_RCP in data:
                value = data.get( ModbusConsts.SLR_RCP )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_RCP, value )

            if ModbusConsts.SLR_COSFI in data:
                value = data.get( ModbusConsts.SLR_COSFI )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_COSFI, value )

            if ModbusConsts.SLR_PF in data:
                value = data.get( ModbusConsts.SLR_PF )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_PF, value )

            if ModbusConsts.SLR_WATTHT in data:
                value = data.get( ModbusConsts.SLR_WATTHT )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_WATTHT, value )

            if ModbusConsts.SLR_RUNTT in data:
                value = data.get( ModbusConsts.SLR_RUNTT )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_RUNTT, value )

            if ModbusConsts.SLR_WATTH in data:
                value = data.get( ModbusConsts.SLR_WATTH )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_WATTH, value )

            if ModbusConsts.SLR_RUNT in data:
                value = data.get( ModbusConsts.SLR_RUNT )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_RUNT, value )

            if ModbusConsts.SLR_OP_STATE in data:
                value = data.get( ModbusConsts.SLR_OP_STATE )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_OP_STATE, value )

            if ModbusConsts.SLR_REC_TIME in data:
                value =  data.get( ModbusConsts.SLR_REC_TIME )
                xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_REC_TIME, value )

            for i in range( 1, 11 ):
                key_volt = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCV + '_' + str(i)
                key_amp  = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCA + '_' + str(i)
                key_pow  = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCW + '_' + str(i)

                if key_volt in data or key_amp in data or key_pow in data:
                    xmlPayload = xmlPayload + '<' + ModbusConsts.SLR_DCIP + ' V=\'' + str(i) + '\'>'
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_DCV, data.get( key_volt ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_DCA, data.get( key_amp ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_DCW, data.get( key_pow ) )
                    xmlPayload = xmlPayload + '</' + ModbusConsts.SLR_DCIP + '>'

            for i in range( 1, 11 ):
                key_volt = ModbusConsts.SLR_MDCIP + '_' + ModbusConsts.SLR_DCV + '_' + str(i)
                key_amp  = ModbusConsts.SLR_MDCIP + '_' + ModbusConsts.SLR_DCA + '_' + str(i)
                key_pow  = ModbusConsts.SLR_MDCIP + '_' + ModbusConsts.SLR_DCW + '_' + str(i)

                if key_volt in data or key_amp in data or key_pow in data:
                    xmlPayload = xmlPayload + '<' + ModbusConsts.SLR_MDCIP + ' V=\'' + str(i) + '\'>'
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_DCV, data.get( key_volt ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_DCA, data.get( key_amp ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_DCW, data.get( key_pow ) )
                    xmlPayload = xmlPayload + '</' + ModbusConsts.SLR_MDCIP + '>'

            for i in range( 1, 11 ):
                key_volt = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACV + '_' + str(i)
                key_amp  = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACA + '_' + str(i)
                key_pow  = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACW + '_' + str(i)
                key_freq = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_FRQ + '_' + str(i)

                if key_volt in data or key_amp in data or key_pow in data or key_freq in data:
                    xmlPayload = xmlPayload + '<' + ModbusConsts.SLR_ACOP + ' V=\'' + str(i) + '\'>'
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ACV, data.get( key_volt ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ACA, data.get( key_amp ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ACW, data.get( key_pow ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_FRQ, data.get( key_freq ) )
                    xmlPayload = xmlPayload + '</' + ModbusConsts.SLR_ACOP + '>'

            for i in range( 1, 11 ):
                key_volt = ModbusConsts.SLR_MACOP + '_' + ModbusConsts.SLR_ACV + '_' + str(i)
                key_amp  = ModbusConsts.SLR_MACOP + '_' + ModbusConsts.SLR_ACA + '_' + str(i)
                key_pow  = ModbusConsts.SLR_MACOP + '_' + ModbusConsts.SLR_ACW + '_' + str(i)
                key_freq = ModbusConsts.SLR_MACOP + '_' + ModbusConsts.SLR_FRQ + '_' + str(i)

                if key_volt in data or key_amp in data or key_pow in data or key_freq in data:
                    xmlPayload = xmlPayload + '<' + ModbusConsts.SLR_MACOP + ' V=\'' + str(i) + '\'>'
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ACV, data.get( key_volt ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ACA, data.get( key_amp ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_ACW, data.get( key_pow ) )
                    xmlPayload = xmlPayload + self.createXmlTag( ModbusConsts.SLR_FRQ, data.get( key_freq ) )
                    xmlPayload = xmlPayload + '</' + ModbusConsts.SLR_MACOP + '>'

            alarms = decodedData.get( ModbusConsts.ALARM )

            xmlPayload = xmlPayload + '<alarms>'

            for alr in alarms:
                xmlPayload = xmlPayload + '<alarm>' + alr + '</alarm>'

            xmlPayload = xmlPayload + '</alarms>'

        except Exception as e:
            pass

        xmlPayload = xmlPayload + '</SINV>'

        return xmlPayload
