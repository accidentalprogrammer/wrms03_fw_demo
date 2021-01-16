#!/usr/bin/env python

##
#  @package AlarmProcessor Package contains the functions to process the alarms and store them in an array
#  depending upon whether the alarm is active or not
#


import logging
from ModbusConsts import ModbusConsts

class AlarmProcessor:

    LOG = logging.getLogger( __name__ )

    ##
    #  Function to process the alarms and sore active alarms in an array
    #
    #  @param decodedData dictionary: dictionary containing the decoded parameters and alarms
    #  @param deviceType string: type of the device
    #
    def processAlarms( self, decodedData, deviceType ):
        for deviceData in decodedData:
            alarmsDict = deviceData.get( ModbusConsts.ALARM )
            if alarmsDict is None:
                return decodedData

            alarmSet = set()
            if deviceType in ModbusConsts.CUSTOM_ALARM_PROCESSORS:
                pass
            else:
                for alr,alrVal in alarmsDict.items():
                    if alrVal == 1:
                        alarmSet.add(alr)
            deviceData[ModbusConsts.ALARM] = list(alarmSet)

        return decodedData
