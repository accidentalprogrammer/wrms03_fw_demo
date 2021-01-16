#!/usr/bin/env python


##
#  @package SensorMeteo Package contains the method to create the CSV payload for METEO sensor
#

import logging
from ModbusConsts import ModbusConsts

class SensorMeteo:

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

            if "IRRADIANCE" in data:
                value = data.get( "IRRADIANCE" )
                labels.append(f'IRRADIANCE_{slaveId}')
                values.append(value)

            if "CELL_TEMP" in data:
                value = data.get( "CELL_TEMP" )
                labels.append(f'CELL_TEMP_{slaveId}')
                values.append(value)

            if "EXT_TEMP" in data:
                value = data.get( "EXT_TEMP" )
                labels.append(f'EXT_TEMP_{slaveId}')
                values.append(value)

        except Exception as e:
            pass

        return (labels,values)

