#!/usr/bin/env python

##
#  @package MessageComposer Module contains the Logic for the the payload construction


import logging
import datetime
import time
import InputDataQueue
from ModbusConsts import ModbusConsts
from SolarInverterXml import SolarInverterXml
import PeriodicTimer
import threading
from PayloadQueue import PayloadQueue
import simplejson as json
import Status
from MainConfig import MainConfig
from Constants import Constants
from WeatherStationXml import WeatherStationXml
from WeatherStationJson import WeatherStationJson
from SolarInverterJson import SolarInverterJson
from Abb33InverterXml import AbbInverter33Xml
from Abb100InverterXml import AbbInverter100Xml
from PayloadProcessor import SolarInverterProcessor
from PayloadProcessor import WSTSensorProcessor
from TcsJsonPayload import TcsJsonPayload
from SolarInverterMeteo import SolarInverterMeteo
from SensorMeteo import SensorMeteo
import GsmUtility

stop = False

class MessageComposer ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    def __init__( self ):
        threading.Thread.__init__( self )

    def run( self ):
        global stop

        while True:
            Status.messageComposerWorking = True
            if stop:
                self.LOG.info( 'Got stop signal from the main module. Thread will be stopped. ' )
                break
            payloadCount = PeriodicTimer.payloadCount
            payload = self.getPayload()
            mc = MainConfig().getConfig()
            payloadType = 'xml' if mc.get( Constants.PAYLOAD_TYPE ) is None else mc.get( Constants.PAYLOAD_TYPE )

            if payloadType == Constants.PAYLOAD_TYPE_TCS:
                try:
                    for pl in payload:
                        pq = PayloadQueue()
                        pq.appendPayload( json.dumps(pl) )
                        self.LOG.debug('Payload: %s ', json.dumps(pl))

                    self.LOG.debug('payload count: %s', PeriodicTimer.payloadCount)
                    if payloadCount == PeriodicTimer.payloadCount and PeriodicTimer.counter >= 0:
                        time.sleep( PeriodicTimer.counter + 1 )
                except Exception as e:
                    self.LOG.error('Error appending payload to queue: %s', e)
            else:
                try:
                    payload = self.preProcessPayload( payload )
                    pq = PayloadQueue()
                    pq.appendPayload( payload )
                    self.LOG.debug( 'Payload: %s', payload )
                    self.LOG.debug('payload count: %s', PeriodicTimer.payloadCount)
                    if payloadCount == PeriodicTimer.payloadCount and PeriodicTimer.counter >= 0:
                        time.sleep( PeriodicTimer.counter + 1 )
                except Exception as e:
                    self.LOG.error('Error appending payload to queue: %s', e)

    ##
    #  Function to get the payload
    def getPayload( self ):
        mc = MainConfig().getConfig()
        payloadType = 'xml' if mc.get( Constants.PAYLOAD_TYPE ) is None else mc.get( Constants.PAYLOAD_TYPE )
        if payloadType == Constants.PAYLOAD_TYPE_XML:
            return self.constructXmlPayload()
        elif payloadType == Constants.PAYLOAD_TYPE_JSON:
            return self.constructJsonPayload()
        elif payloadType == 'meteo':
            return self.constructMeteoPayload()
        else:
            return self.constructXmlPayload()


    ##
    #  Function to construct the XML payload for all the data received from different types of devices
    def constructXmlPayload( self ):

        recordTime = PeriodicTimer.recordTimestamp
        mc = MainConfig().getConfig()
        if Constants.GATEWAY_ID in mc:
            xmlPayload = '<GATEWAY_ID V=\'' + mc.get( Constants.GATEWAY_ID ) + '\'>'
        else:
            xmlPayload = '<GATEWAY_ID V=\'' + Status.deviceId + '\'>'
        xmlPayload = xmlPayload + '<DT V=\'' + recordTime + '\'>'
        #xmlPayload = xmlPayload + '<UID V=\'' + GsmUtility.ImeiNumber + '\'/>'
        modbusPayloadConstructed = False


        while True:
            if not InputDataQueue.modbusDataQueue.empty() and  not modbusPayloadConstructed:
                modbusDataList = InputDataQueue.modbusDataQueue.get_nowait()
                modbusPayloadConstructed = True
                self.LOG.debug( 'Modbus data from queue: %s', modbusDataList )
                for modbusData in modbusDataList:
                    devCategory = modbusData.get( ModbusConsts.DEVICE_CATEGORY )
                    if ModbusConsts.CAT_INVERTER == devCategory:
                        inverterPayload = None
                        try:
                            inverterPayload = SolarInverterXml().getXmlPayload( modbusData, recordTime )
                        except Exception as e:
                            self.LOG.error( 'Error Constructing inverter payload: %s', e )

                        if inverterPayload is not None:
                            xmlPayload = xmlPayload + inverterPayload

                    elif ModbusConsts.CAT_WST == devCategory:
                        wstPayload = None
                        try:
                            wstPayload = WeatherStationXml().getXmlPayload( modbusData, recordTime )
                        except Exception as e:
                            self.LOG.error('Error constructing Weather Station payload: %s', e )

                        if wstPayload is not None:
                            xmlPayload = xmlPayload + wstPayload

                    elif ModbusConsts.CAT_INVERTER_ABB33 == devCategory:
                        abbPayload = None
                        try:
                            abbPayload = AbbInverter33Xml().getXmlPayload( modbusData, recordTime )
                        except Exception as e:
                            self.LOG.error( 'Error constructing Abb 33 KW inverter payload: %s', e )

                        if abbPayload is not None:
                            xmlPayload = xmlPayload + abbPayload

                    elif ModbusConsts.CAT_INVERTER_ABB100 == devCategory:
                        abbPayload = None
                        try:
                            abbPayload = AbbInverter100Xml().getXmlPayload( modbusData, recordTime )
                        except Exception as e:
                            self.LOG.error( 'Error constructing Abb 100 KW inverter payload: %s', e )

                        if abbPayload is not None:
                            xmlPayload = xmlPayload + abbPayload

                InputDataQueue.modbusDataQueue.task_done()
            if PeriodicTimer.counter > 10 and not modbusPayloadConstructed:
                time.sleep( 5.0 )
            else:
                break

        xmlPayload = xmlPayload + '</DT>'
        xmlPayload = xmlPayload + '</GATEWAY_ID>'

        return xmlPayload


    def constructJsonPayload( self ):

        recordTime = str(PeriodicTimer.recordTimestamp)
        print(recordTime)

        modbusPayloadConstructed = False

        gatewayPayload = {}
        gatewayPayload[Status.deviceId] = []

        payload = {}
        payload['DT'] = recordTime
        payload['imei'] = GsmUtility.ImeiNumber
        while True:
            if not InputDataQueue.modbusDataQueue.empty() and  not modbusPayloadConstructed:
                modbusDataList = InputDataQueue.modbusDataQueue.get_nowait()
                modbusPayloadConstructed = True
                for modbusData in modbusDataList:
                    devType = modbusData.get( ModbusConsts.DEVICE_TYPE )
                    slaveId = modbusData.get( ModbusConsts.SLAVE_ID )
                    devCategory = modbusData.get( ModbusConsts.DEVICE_CATEGORY )
                    if devCategory == ModbusConsts.CAT_WST:
                        devPayloadArr = []
                        if devCategory in payload:
                            devPayloadArr = payload.get(devCategory)
                        devPayloadArr.append( WeatherStationJson().getJsonPayload( modbusData, recordTime ) )
                        payload[devCategory] = devPayloadArr
                    elif devCategory == ModbusConsts.CAT_INVERTER:
                        devPayloadArr = []
                        if 'inverters' in payload:
                            devPayloadArr = payload.get('inverters')
                        devPayloadArr.append( SolarInverterJson().getJsonPayload( modbusData, recordTime ) )
                        payload['inverters'] = devPayloadArr
                InputDataQueue.modbusDataQueue.task_done()
            if PeriodicTimer.counter > 10 and not modbusPayloadConstructed:
                time.sleep( 5.0 )
            else:
                break

        gPayload = gatewayPayload.get( Status.deviceId )
        gPayload.append(payload)
        jsonPayload = json.dumps(gatewayPayload)
        return jsonPayload


    ##
    #
    def constructTcsPayload( self ):

        recordTime = str(PeriodicTimer.recordTimestamp)
        print(recordTime)

        modbusPayloadConstructed = False

        tcsPayloadList = []

        while True:
            if not InputDataQueue.modbusDataQueue.empty() and  not modbusPayloadConstructed:
                modbusDataList = InputDataQueue.modbusDataQueue.get_nowait()
                modbusPayloadConstructed = True
                # Call TcsPayloadConstructor here
                tcsPayloadList = TcsJsonPayload().constructPayload(modbusDataList, recordTime)
                InputDataQueue.modbusDataQueue.task_done()
            if PeriodicTimer.counter > 10 and not modbusPayloadConstructed:
                time.sleep( 5.0 )
            else:
                break

        return tcsPayloadList


    def constructMeteoPayload( self ):

        recordTime = str(PeriodicTimer.recordTimestamp)
        print(recordTime)

        modbusPayloadConstructed = False

        gatewayPayload = {}
        gatewayPayload[Status.deviceId] = []

        payload = ''
        payload += 'xyz ltd\n'
        payload += 'meteo control\n'
        labelsComb = []
        valuesComb = []
        labelsComb.append('DateTime')
        valuesComb.append(recordTime)
        while True:
            if not InputDataQueue.modbusDataQueue.empty() and  not modbusPayloadConstructed:
                modbusDataList = InputDataQueue.modbusDataQueue.get_nowait()
                modbusPayloadConstructed = True
                for modbusData in modbusDataList:
                    devType = modbusData.get( ModbusConsts.DEVICE_TYPE )
                    slaveId = modbusData.get( ModbusConsts.SLAVE_ID )
                    devCategory = modbusData.get( ModbusConsts.DEVICE_CATEGORY )
                    if devCategory == ModbusConsts.CAT_INVERTER:
                        labels, values = SolarInverterMeteo().getMeteoPayload( modbusData, recordTime )
                        labelsComb += labels
                        valuesComb += values
                    if devCategory == ModbusConsts.CAT_WST:
                        labels, values = SensorMeteo().getMeteoPayload( modbusData, recordTime )
                        labelsComb += labels
                        valuesComb += values
                InputDataQueue.modbusDataQueue.task_done()
            if PeriodicTimer.counter > 10 and not modbusPayloadConstructed:
                time.sleep( 5.0 )
            else:
                break

        labelsStr = ';'.join( [ str(x) for x in labelsComb ] ).strip()
        valuesStr = ';'.join( [ str(x) for x in valuesComb ] ).strip()
        payload += labelsStr +'\n'
        payload += valuesStr + '\n'
        return payload

    ##
    #
    def preProcessPayload( self, payload ):

        mc = MainConfig().getConfig()
        payloadType = mc.get( Constants.PAYLOAD_TYPE )
        if payloadType == Constants.PAYLOAD_TYPE_XML:
            sp = SolarInverterProcessor()

            # Populate the today energy in the solar inverter payload
            newPayload = sp.populateTodayEnergy( payload )
            if newPayload is not None:
                payload = newPayload.decode('utf-8')

            wstProc = WSTSensorProcessor()

            # Merge the multiple WST into single
            newPayload = wstProc.mergeWSt( payload )
            if newPayload is not None:
                payload = newPayload.decode('utf-8')

        if payloadType == Constants.PAYLOAD_TYPE_JSON:

            try:
                payloadJson = json.loads(payload)
                sp = SolarInverterProcessor()

                newPayload = sp.populateTodayEnergyJson( payloadJson )
                if newPayload is not None:
                    payloadJson = newPayload

                payload = json.dumps(payloadJson)
            except Exception as e:
                self.LOG.error('Error preprocessing Solar Inverter: %s', e)                

            try:
                payloadJson = json.loads(payload)
                wstProc = WSTSensorProcessor()

                newPayload = wstProc.mergeWstJson( payloadJson )
                if newPayload is not None:
                    payloadJson = newPayload

                payload = json.dumps(payloadJson)
            except Exception as e:
                self.LOG.error('Error merging WSTs %s', e)


        return payload
