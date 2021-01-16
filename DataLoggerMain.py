#!/usr/bin/env python

##
#  @package DataLoggerMain This is the main module where the application starts
#  It creates the different threads for the data acquisition and sending
#

import ModbusDataService
import PeriodicTimer
import MessageComposer
import MessageSender
import GsmUtility
from MainConfig import MainConfig
from Constants import Constants
import time
import Status
from ModbusDeviceList import ModbusDeviceList
import ProcessMonitor
import logging.config
import logging
from LogConfig import LogConfig
import OPi.GPIO as GPIO
import datetime
from PayloadQueue import PayloadQueue
import LoraUtility
import LedStatus
import simplejson as json
import subprocess
from ModbusCommandSender import ModbusCommandSender
from SerialConnection import SerialConnection
import ModbusLib




def main():
    imei = None
    mc = MainConfig().getConfig()

    #GsmUtility.resetModem()
    try:
        subprocess.call( 'hwclock -f /dev/rtc1 -s', shell=True )
    except Exception as e:
        self.LOG.error( 'Error syncing time: %s', e )

    try:
        imei = GsmUtility.getGsmImeiNumber()
    except Exception as e:
        print(e)

    try:
        ser = SerialConnection().getSerialConnection( connParams.get( ModbusConsts.BAUDRATE ) ,
                                                      connParams.get( ModbusConsts.PARITY ),
                                                      connParams.get( ModbusConsts.STOP_BITS ),
                                                      connParams.get( ModbusConsts.BYTE_SIZE ))
        command = 'FA0600060001'
        crc = ModbusLib.get_modbus_crc( bytearray.fromhex( command ) )
        command = command+crc
        print('UPS command', command)
        commandResp = ModbusCommandSender().sendCommand( ser, command, 'RTU' )
        if commandResp:
            print('UPS written successfully')
        else:
            print('Error  writing to UPS')
    except Exception as e:
        print('Error writing to UPS', e)

    GsmUtility.ImeiNumber = '0123456789' if imei is None else imei

    Status.deviceId = '0123456789' if mc.get( Constants.DEVICE_ID ) is None else mc.get( Constants.DEVICE_ID )

    try:
        with open( '/fw/DataLogger/app/version.info', 'r' ) as f:
            Status.fwVersion = f.readline()
            Status.fwVersion = Status.fwVersion.strip()
    except Exception as e:
        print( 'Error reading Firmware version: %s', e )


    recordTime = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    payload_type = 'xml' if mc.get( Constants.PAYLOAD_TYPE ) is None else mc.get( Constants.PAYLOAD_TYPE )
    if payload_type == Constants.PAYLOAD_TYPE_XML:
        initialRecord = '<GATEWAY_ID V=\'' + str(Status.deviceId) + '\'>' + '<DT V=\'' + recordTime + '\'>' + '<FW_VERSION V=\''+ str(Status.fwVersion) +'\'/></DT></GATEWAY_ID>'
    elif payload_type == Constants.PAYLOAD_TYPE_JSON:
        initialRecord = {}
        initialRecord['gateway_id'] = Status.deviceId
        initialRecord['dt'] = recordTime
        initialRecord['fw_version'] = Status.fwVersion
        initialRecord['imei'] = GsmUtility.ImeiNumber
        initialRecord = json.dumps(initialRecord)
    else:
        initialRecord = '<GATEWAY_ID V=\'' + str(Status.deviceId) + '\'>' + '<DT V=\'' + recordTime + '\'>' + '<FW_VERSION V=\''+ str(Status.fwVersion) +'\'/></DT></GATEWAY_ID>'

    pq = PayloadQueue()
    pq.appendPayload( initialRecord )


    Status.modbusDevStatus = [0] * len( ModbusDeviceList().getModbusDeviceList() )
    print('No of modbus devices ', len( ModbusDeviceList().getModbusDeviceList() ) )
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT)

    GPIO.setup(22, GPIO.OUT)

    GPIO.output(22, GPIO.HIGH)
    time.sleep(5)

    GPIO.setup(8, GPIO.OUT)
    GPIO.output(8,GPIO.HIGH)
    time.sleep(5)
    try:
        channel = mc.get( Constants.LORA_CHANNEL )
        channel = 23 if channel is None else channel
        result = LoraUtility.setChannel( channel )
        print('Lora Channel Result: ', result)
    except Exception as e:
        print(e)

    GPIO.output(8, GPIO.LOW)

    # Start the process monitor thread
    pm = ProcessMonitor.ProcessMonitor()
    pm.start()

    interval = int(mc.get( Constants.PERIODIC_INTERVAL ))
    curtime = time.time()
    timeToSleep = interval - ( curtime % interval )
    time.sleep( timeToSleep )

    # Start the PeriodicTimer
    pt = PeriodicTimer.PeriodicTimer()
    pt.start()

    time.sleep( 1 )

    # Start the modbus data acquisition service
    modbusDataService = ModbusDataService.ModbusDataService()
    modbusDataService.start()


    # Start the payload construction service
    messageComposer = MessageComposer.MessageComposer()
    messageComposer.start()


    # Start the Message sending service
    messageSender = MessageSender.MessageSender()
    messageSender.start()



    # Start the LED thread
    ledt = LedStatus.LedStatus()
    ledt.start()

    # Wait for the threads to complete
    while True:
        if Status.stop:
            MessageSender.stop = True
            MessageComposer.stop = True
            ModbusDataService.stop = True
            PeriodicTimer.stop = True
            ProcessMonitor.stop = True
            time.sleep( int( MainConfig().getConfig().get( Constants.PERIODIC_INTERVAL ) ) )
            break
        else:
            time.sleep( int( MainConfig().getConfig().get( Constants.PERIODIC_INTERVAL ) ) )

if __name__== "__main__":
    print( LogConfig().getConfig() )
    logging.config.dictConfig( LogConfig().getConfig() )
    LOG = logging.getLogger( __name__ )
    LOG.debug( 'Starting the Data Logger' )
    main()

#pt.join()
#modbusDataService.join()
#messageComposer.join()
#messageSender.join()

