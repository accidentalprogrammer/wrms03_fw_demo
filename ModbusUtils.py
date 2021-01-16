#!/usr/bin/env python


##
#  @package ModbusUtils Module contains the various functions required for decoding the Modbus data
#

import logging

LOG = logging.getLogger( __name__ )


def reverseTwoElements( data ):
    if len( data ) % 2 != 0:
        LOG.warn( "Data is not in multiple of 2" )
        return data

    newdata = []
    newdata.append(data[2])
    newdata.append(data[3])
    newdata.append(data[0])
    newdata.append(data[1])
    return newdata
    # swap 1st and 3rd byte
    temp = data[0]
    data[0] = data[2]
    data[2] = temp

    # swap 2nd and 4th byte
    temp = data[1]
    data[1] = data[3]
    data[3] = temp

    return data


##
#
def bytesToInt( data ):
    length = len( data )
    intVal = 0
    for i in range( 0, length ):
        intVal = intVal << 8
        intVal = intVal | data[i]
    return intVal
