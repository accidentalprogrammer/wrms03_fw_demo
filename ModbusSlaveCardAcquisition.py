#!/usr/bin/env python

##
#  @package ModbusSlaveCardAcquisition Module contains the code to communicate with the slave card and
#  get the controller data
#

import logging
from ModbusConsts import ModbusConsts
from SerialConnection import SerialConnection
from LoraConnection import LoraConnection
import time
import Status

class ModbusSlaveCardAcquisition:

    LOG = logging.getLogger( __name__ )

    ##
    #
    def querySlaveCard( self, modbusDevice, ser, devIndex ):

        devType = modbusDevice.get( ModbusConsts.DEVICE_TYPE )
        if devType == ModbusConsts.DEVICE_TYPE_DELTA:
            return self.getDelta(modbusDevice, ser, devIndex)
        elif devType == ModbusConsts.DEVICE_TYPE_SLAVE_SENSOR:
            pass
        elif devType == ModbusConsts.DEVICE_TYPE_ABB33:
            return self.getAbb_33(modbusDevice, ser, devIndex)
        elif devType == ModbusConsts.DEVICE_TYPE_ABB100:
            return self.getAbb_100(modbusDevice, ser, devIndex)


    ##
    #
    def getAbb( self, modbusDevice, devIndex ):
        pass

    ##
    #
    def getSensorData( self, modbusDevice, ser, devIndex ):
        numberOfData =[32]
        funId = [ 4 ]
        sor = [ 0 ]
        response = {}
        for i in range( 0, 10 ):
            slaveCardId = modbusDevice.get( ModbusConsts.SLAVE_CARD_ID )
            invId = ("%02X"%slaveCardId).upper()
            command = str( i ).zfill( 2 )
            queryString = "$" + invId + "DF" + command + "#"
            ser.write( queryString )
            time.sleep( 0.008 )
            ser.flushOutput()
            time.sleep( 2 )
            size = ser.inWaiting()
            data = ser.readline()
            valData = None
            if "?" in data and "!" in data and queryString in data:
                data = data[data.find('?')+1 : data.find('!')]
                if("NRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='NO RESPONSE'/>"
                    recCount = 5
                    pass
                if("IRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='INVALID RESPONSE'/>"
                    recCount = 5
                    pass
                if(len(data) ==  numberOfData[i]+8):
                    valData = data.replace( queryString, "" )

            if valData is None:
                Status.modbusDevStatus[ devIndex ] += 1
            else:
                Status.modbusDevStatus[ devIndex ] = 0

            respKey = "%02X"%funId[ i ] + "%04X"%sor[ i ]
            response[ respKey ] = data

        ser.close()
        return response



    ##
    #
    def getDelta( self, modbusDevice, ser, devIndex ):
        numberOfData =[32,76,72,52,48,20,44,12,96,40]
        funId = [ 4, 4, 4, 4, 4, 4, 4, 4, 4, 4 ]
        sor = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        response = {}
        ser = None
        for i in range( 0, 10 ):
            slaveCardId = modbusDevice.get(ModbusConsts.CONN_PARAMS).get( ModbusConsts.SLAVE_CARD_ID )
            invId = ("%02X"%int(slaveCardId)).upper()
            command = str( i ).zfill( 2 )
            queryStr = invId + "DF" + command
            queryString = "$" + invId + "DF" + command + "#"
            ser.write( queryString.encode() )
            time.sleep( 0.008 )
            ser.flushOutput()
            time.sleep( 2 )
            size = ser.inWaiting()
            data = ser.read(size)
            data = data.decode('utf-8')
            valData = None
            if '?' in data and '!' in data and queryStr in data:
                data = data[data.find('?')+1 : data.find('!')]
                if("NRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='NO RESPONSE'/>"
                    recCount = 5
                    pass
                if("IRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='INVALID RESPONSE'/>"
                    recCount = 5
                    pass
                if(len(data) ==  numberOfData[i]+8):
                    valData = data.replace( queryStr, "" )
                    valData = valData[2:]

            if valData is None:
                Status.modbusDevStatus[ devIndex ] += 1
            else:
                Status.modbusDevStatus[ devIndex ] = 0

            respKey = "%02X"%funId[ i ] + "_" + "%04X"%sor[ i ]
            response[ respKey ] = bytearray.fromhex( valData )

        ser.close()
        return response

    ##
    #
    def getAbb_33( self, modbusDevice,ser, devIndex ):
#        numberOfData =[32,76,72,52,48,20,44,12,96,40]
        funId = [ 4, 4, 4, 4, 4 ]
        sor = [ 0, 1, 2, 3, 4 ]
        response = {}
        print('Querying Device: ', modbusDevice)
        for i in range( 0, 5 ):
            slaveCardId = modbusDevice.get(ModbusConsts.CONN_PARAMS).get( ModbusConsts.SLAVE_CARD_ID )
            invId = ("%02X"%int(slaveCardId)).upper()
            command = str( i ).zfill( 2 )
            queryStr = invId + "DF" + command
            queryString = "$" + invId + "DF" + command + "#"
            ser.write( queryString.encode() )
            time.sleep( 0.008 )
            ser.flushOutput()
            time.sleep( 2 )
            size = ser.inWaiting()
            data = ser.read(size)
            data = data.decode('utf-8')
            valData = None
            if '?' in data and '!' in data and queryStr in data:
                data = data[data.find('>')+1 : data.find('!')]
                if i == 0:
                    data = data[:data.find('<')]
                print(data)
                if("NRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='NO RESPONSE'/>"
                    recCount = 5
                    pass
                if("IRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='INVALID RESPONSE'/>"
                    recCount = 5
                    pass
            valData = data.replace( " ", "" )

            if valData is None:
                Status.modbusDevStatus[ devIndex ] += 1
            else:
                Status.modbusDevStatus[ devIndex ] = 0

            respKey = "%02X"%funId[ i ] + "_" + "%04X"%sor[ i ]
            response[ respKey ] = None if valData is None else bytearray.fromhex(valData)

        ser.close()
        return response



    ##
    #
    def getAbb_100( self, modbusDevice,ser, devIndex ):
        numberOfData =[32,76,72,52,48,20,44,12,96,40]
        funId = [ 4, 4, 4, 4, 4 ]
        sor = [ 0, 1, 2, 3, 4 ]
        response = {}
        for i in range( 0, 5 ):
            slaveCardId = modbusDevice.get(ModbusConsts.CONN_PARAMS).get( ModbusConsts.SLAVE_CARD_ID )
            invId = ("%02X"%int(slaveCardId)).upper()
            command = str( i ).zfill( 2 )
            queryStr = invId + "DF" + command
            queryString = "$" + invId + "DF" + command + "#"
            ser.write( queryString.encode() )
            time.sleep( 0.008 )
            ser.flushOutput()
            time.sleep( 2 )
            size = ser.inWaiting()
            data = ser.read(size)
            data = data.decode('utf-8')
            valData = None
            if '?' in data and '!' in data and queryStr in data:
                data = data[data.find('>')+1 : data.find('!')]
                if i == 0:
                    data = data[:data.find('<')]
                print(data)
                if("NRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='NO RESPONSE'/>"
                    recCount = 5
                    pass
                if("IRSP" in data):
                    strUpload +="<QRY"+str(i)+" V='INVALID RESPONSE'/>"
                    recCount = 5
                    pass
                valData = data.replace( " ", "" )

            if valData is None:
                Status.modbusDevStatus[ devIndex ] += 1
            else:
                Status.modbusDevStatus[ devIndex ] = 0

            respKey = "%02X"%funId[ i ] + "_" + "%04X"%sor[ i ]
            response[ respKey ] = None if valData is None else bytearray.fromhex(valData)

        ser.close()
        return response
