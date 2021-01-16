#!/usr/bin/env python


##
#  @package SolarInverterJson Package contains the method to create the Json payload for the solar inverter
#

import logging
from ModbusConsts import ModbusConsts

class SolarInverterMeteo:

    LOG = logging.getLogger( __name__ )



    ##
    #
    def getMeteoPayload( self, decodedData, recordTime ):

        labels = []
        values = []
        slaveId = decodedData.get( ModbusConsts.SLAVE_ID )
        
        try:
            data = decodedData.get( ModbusConsts.DATA )
            print("data in CSV: ", data)

            if ModbusConsts.SLR_WATTHT in data:
                value = data.get( ModbusConsts.SLR_WATTHT )
                labels.append(f'Inv{slaveId}_Daily_energy')
                values.append(value)

            if ModbusConsts.SLR_OPPWR in data:
                value = data.get( ModbusConsts.SLR_OPPWR )
                labels.append(f'Inv{slaveId}_AC_Power')
                values.append(value)

            if ModbusConsts.SLR_IPPWR in data:
                value = data.get( ModbusConsts.SLR_IPPWR )
                labels.append(f'Inv{slaveId}_DC_Power')
                values.append(value)

            acVolt = []
            for i in range(1,4):
                key = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACV + '_' + str(i)
                labels.append(f'Inv{slaveId}_AC_Volt_{i}')
                values.append( data.get( key ) )

            acCur = []
            for i in range(1,4):
                key = ModbusConsts.SLR_ACOP + '_' + ModbusConsts.SLR_ACA + '_' + str(i)
                labels.append(f'Inv{slaveId}_AC_Current_{i}')
                values.append( data.get( key ) )

            dcVolt = []
            for i in range(1,11):
                key = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCV + '_' + str(i)
                if key in data:
                    labels.append(f'Inv{slaveId}_DC_Volt_{i}')
                    values.append( data.get( key ) )

            dcCurrent = []
            for i in range(1,11):
                key = ModbusConsts.SLR_DCIP + '_' + ModbusConsts.SLR_DCA + '_' + str(i)
                if key in data:
                    labels.append(f'Inv{slaveId}_DC_Current_{i}')
                    values.append( data.get( key ) )

        except Exception as e:
            pass

        return (labels,values)

