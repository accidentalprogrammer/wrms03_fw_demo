#!/usr/bin/env python


##
#  @package SolarInverterJson Package contains the method to create the Json payload for the solar inverter
#

import logging
from ModbusConsts import ModbusConsts

class SolarInverterJson:

    LOG = logging.getLogger( __name__ )



    ##
    #
    def getJsonPayload( self, decodedData, recordTime ):

        jsonPayload = {}
        jsonPayload[ModbusConsts.SLAVE_ID] = decodedData.get( ModbusConsts.SLAVE_ID )
        jsonPayload[ModbusConsts.DEVICE_TYPE] = decodedData.get( ModbusConsts.DEVICE_TYPE )
        jsonPayload[ModbusConsts.DEVICE_CATEGORY] = decodedData.get( ModbusConsts.DEVICE_CATEGORY )
        jsonPayload[ModbusConsts.DEVICE_ID] = decodedData.get( ModbusConsts.DEVICE_ID )
        #jsonPayload = {}

        try:
            data = decodedData.get( ModbusConsts.DATA )
            print("data in solarJson: ", data)

            if ModbusConsts.SLR_IPPWR in data:
                value = data.get( ModbusConsts.SLR_IPPWR )
                jsonPayload['total_dcp'] = value

            if ModbusConsts.SLR_OPPWR in data:
                value = data.get( ModbusConsts.SLR_OPPWR )
                jsonPayload['total_acp'] = value

            if ModbusConsts.SLR_APP in data:
                value = data.get( ModbusConsts.SLR_APP )
                jsonPayload['app_power'] = value

            if ModbusConsts.SLR_RCP in data:
                value = data.get( ModbusConsts.SLR_RCP )
                jsonPayload['react_power'] = value

            if ModbusConsts.SLR_COSFI in data:
                value = data.get( ModbusConsts.SLR_COSFI )
                jsonPayload['pf'] = value

            if ModbusConsts.SLR_WATTHT in data:
                value = data.get( ModbusConsts.SLR_WATTHT )
                jsonPayload['today_energy'] = value

            if ModbusConsts.SLR_RUNTT in data:
                value = data.get( ModbusConsts.SLR_RUNTT )
                jsonPayload['today_runt'] = value

            if ModbusConsts.SLR_WATTH in data:
                value = data.get( ModbusConsts.SLR_WATTH )
                jsonPayload['total_energy'] = value

            if ModbusConsts.SLR_RUNT in data:
                value = data.get( ModbusConsts.SLR_RUNT )
                jsonPayload['total_runt'] = value

            if ModbusConsts.SLR_OP_STATE in data:
                value = data.get( ModbusConsts.SLR_OP_STATE )
                jsonPayload['op_state'] = value

            acVolt = []
            for i in range(1,4):
                key = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACV + '_' + str(i)
                acVolt.append( data.get( key ) )
            jsonPayload['ac_volt'] = acVolt

            acCur = []
            for i in range(1,4):
                key = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACA + '_' + str(i)
                acCur.append( data.get( key ) )
            jsonPayload['ac_cur'] = acCur

            acFreq = []
            for i in range(1,4):
                key = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_FRQ + '_' + str(i)
                acFreq.append( data.get( key ) )
            jsonPayload['ac_freq'] = acFreq

            acPower = []
            for i in range(1,4):
                key = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACW + '_' + str(i)
                acPower.append( data.get( key ) )
            jsonPayload['ac_power'] = acPower

            dcVolt = []
            for i in range(1,11):
                key = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCV + '_' + str(i)
                if key in data:
                    dcVolt.append( data.get( key ) )
            jsonPayload['dc_volt'] = dcVolt

            dcCurrent = []
            for i in range(1,11):
                key = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCA + '_' + str(i)
                if key in data:
                    dcCurrent.append( data.get( key ) )
            jsonPayload['dc_cur'] = dcCurrent

            dcPower = []
            for i in range(1,11):
                key = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCW + '_' + str(i)
                if key in data:
                    dcPower.append( data.get( key ) )
            jsonPayload['dc_power'] = dcPower

        except Exception as e:
            pass

        return jsonPayload

