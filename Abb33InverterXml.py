#!/usr/bin/env python

import logging
from ModbusConsts import ModbusConsts

class AbbInverter33Xml:
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
            if 'DCV' in data:
                value = data.get( 'DCV' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DCV', value )

            if 'LIC' in data:
                value = data.get( 'LIC' )
                xmlPayload = xmlPayload + self.createXmlTag( 'LIC', value )

            if 'FRQ' in data:
                value = data.get( 'FRQ' )
                xmlPayload = xmlPayload + self.createXmlTag( 'FRQ', value )

            if 'APP' in data:
                value = data.get( 'APP' )
                xmlPayload = xmlPayload + self.createXmlTag( 'APP', value )

            if 'ACP' in data:
                value = data.get( 'ACP' )
                xmlPayload = xmlPayload + self.createXmlTag( 'ACP', value )

            if 'RCP' in data:
                value = data.get( 'RCP' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RCP', value )

            if 'COSFi' in data:
                value = data.get( 'COSFi' )
                xmlPayload = xmlPayload + self.createXmlTag( 'COSFi', value )

            if 'INC' in data:
                value = data.get( 'INC' )
                xmlPayload = xmlPayload + self.createXmlTag( 'INC', value )

            if 'TRIPF' in data:
                value = data.get( 'TRIPF' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TRIPF', value )

            if 'ACTWARN_1' in data:
                value = data.get( 'ACTWARN_1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'ACTWARN_1', value )

            if 'ACTWARN_2' in data:
                value = data.get( 'ACTWARN_2' )
                xmlPayload = xmlPayload + self.createXmlTag( 'ACTWARN_2', value )

            if 'ACTWARN_3' in data:
                value = data.get( 'ACTWARN_3' )
                xmlPayload = xmlPayload + self.createXmlTag( 'ACTWARN_3', value )

            if 'ACTWARN_4' in data:
                value = data.get( 'ACTWARN_4' )
                xmlPayload = xmlPayload + self.createXmlTag( 'ACTWARN_4', value )

            if 'ACTWARN_5' in data:
                value = data.get( 'ACTWARN', value )
                xmlPayload = xmlPayload + self.createXmlTag( 'ACTWARN_5', value )

            if 'LATWARN' in data:
                value = data.get( 'LATWARN' )
                xmlPayload = xmlPayload + self.createXmlTag( 'LATWARN', value )

            if 'MSTBRD' in data:
                value = data.get( 'MSTBRD' )
                xmlPayload = xmlPayload + self.createXmlTag( 'MSTBRD', value )

            if 'CPU_U' in data:
                value = data.get( 'CPU_U' )
                xmlPayload = xmlPayload + self.createXmlTag( 'CPU_U', value )

            if 'CON_STT' in data:
                value = data.get( 'CON_STT' )
                xmlPayload = xmlPayload + self.createXmlTag( 'CON_STT', value )

            if 'RESVD1' in data:
                value = data.get( 'RESVD1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RESVD1', value )

            if 'DISC_DIG' in data:
                value = data.get( 'DISC_DIG' )
                xmlPayload = xmlPayload + self.createXmlTag( 'DISC_DIG', value )

            if 'RSVD2' in data:
                value = data.get( 'RSVD2' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RSVD2', value )

            if 'OPPWR_DIG' in data:
                value = data.get( 'OPPWR_DIG' )
                xmlPayload = xmlPayload + self.createXmlTag( 'OPPWR_DIG', value )

            if 'RSVD3' in data:
                value = data.get( 'RSVD3' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RSVD3', value )

            if 'UPTIME' in data:
                value = data.get( 'UPTIME' )
                xmlPayload = xmlPayload + self.createXmlTag( 'UPTIME', value )

            if 'RSVD4' in data:
                value = data.get( 'RSVD4' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RSVD4', value )

            if 'OP_TIME' in data:
                value = data.get( 'OP_TIME' )
                xmlPayload = xmlPayload + self.createXmlTag( 'OP_TIME', value )

            if 'IN_FANS' in data:
                value = data.get( 'IN_FANS' )
                xmlPayload = xmlPayload + self.createXmlTag( 'IN_FANS', value )

            if 'EX_FAN1S' in data:
                value = data.get( 'EX_FAN1S' )
                xmlPayload = xmlPayload + self.createXmlTag( 'EX_FAN1S', value )

            if 'EX_FAN2S' in data:
                value = data.get( 'EX_FAN2S' )
                xmlPayload = xmlPayload + self.createXmlTag( 'EX_FAN2S', value )

            if 'GRID_CON' in data:
                value = data.get( 'GRID_CON' )
                xmlPayload = xmlPayload + self.createXmlTag( 'GRID_CON', value )

            if 'RSVD5' in data:
                value = data.get( 'RSVD5' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RSVD5', value )

            if 'CB_TEMP' in data:
                value = data.get( 'CB_TEMP' )
                xmlPayload = xmlPayload + self.createXmlTag( 'CB_TEMP', value )

            if 'IN_TEMPA' in data:
                value = data.get( 'IN_TEMPA' )
                xmlPayload = xmlPayload + self.createXmlTag( 'IN_TEMPA', value )

            if 'IN_TEMPB' in data:
                value = data.get( 'IN_TEMPB' )
                xmlPayload = xmlPayload + self.createXmlTag( 'IN_TEMPB', value )

            if 'IN_TEMPC' in data:
                value = data.get( 'IN_TEMPC' )
                xmlPayload = xmlPayload + self.createXmlTag( 'IN_TEMPC', value )

            if 'AMP_1' in data:
                value = data.get( 'AMP_1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_1', value )

            if 'AMP_2' in data:
                value = data.get( 'AMP_2' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_2', value )

            if 'AMP_3' in data:
                value = data.get( 'AMP_3' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_3', value )

            if 'AMP_4' in data:
                value = data.get( 'AMP_4' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_4', value )

            if 'AMP_5' in data:
                value = data.get( 'AMP_5' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_5', value )

            if 'AMP_6' in data:
                value = data.get( 'AMP_6' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_6', value )

            if 'AMP_7' in data:
                value = data.get( 'AMP_7' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_7', value )

            if 'AMP_8' in data:
                value = data.get( 'AMP_8' )
                xmlPayload = xmlPayload + self.createXmlTag( 'AMP_8', value )

            if 'TTL_ENRGY' in data:
                value = data.get( 'TTL_ENRGY' )
                xmlPayload = xmlPayload + self.createXmlTag( 'TTL_ENRGY', value )

            if 'RSVD6' in data:
                value = data.get( 'RSVD6' )
                xmlPayload = xmlPayload + self.createXmlTag( 'RSVD6', value )

            if 'VOLT_U1' in data:
                value = data.get( 'VOLT_U1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VOLT_U1', value )

            if 'VOLT_V1' in data:
                value = data.get( 'VOLT_V1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VOLT_V1', value )

            if 'VOLT_W1' in data:
                value = data.get( 'VOLT_W1' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VOLT_W1', value )

            if 'VOLT_UV' in data:
                value = data.get( 'VOLT_UV' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VOLT_UV', value )

            if 'VOLT_VW' in data:
                value = data.get( 'VOLT_VW' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VOLT_VW', value )

            if 'VOLT_WU' in data:
                value = data.get( 'VOLT_WU' )
                xmlPayload = xmlPayload + self.createXmlTag( 'VOLT_WU', value )
        except Exception as e:
            self.LOG.error( 'Error constructing Abb 33KW inverter payload: %s', e )


        xmlPayload = xmlPayload + '</SINV>'

        return xmlPayload
