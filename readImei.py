#!/usr/bin/env python

import GsmUtility


imei = GsmUtility.getGsmImeiNumber()
currentImei = None

try:
    with open( '/fw/DataLogger/deviceId', 'r' ) as f:
        currentImei = f.readline()
        currentImei = currentImei.strip()
except Exception as e:
    print( 'Error reading Device ID: %s', e )

if imei is not None:
    GsmUtility.ImeiNumber = imei
elif currentImei is not None:
    GsmUtility.ImeiNumber = currentImei
else:
    GsmUtility.ImeiNumber = '0123456789'

try:
    with open( '/fw/DataLogger/deviceId', 'w' ) as f:
        f.write( GsmUtility.ImeiNumber )
except Exception as e:
    print( 'Error storing the Device ID: %s', e )
