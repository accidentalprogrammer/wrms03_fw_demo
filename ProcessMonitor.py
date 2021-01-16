#!/usr/bin/env python


##
#  @package ProcessMonitor Module contains the class implementation which runs in a separate thread and
#  monitors all the threads and other statuses. If any abnormality is found it just reboots the device
#


import threading
import logging
import time
import Status
import UpgradeFw
from Constants import Constants
import subprocess
import GsmUtility
import LedStatus
from PayloadQueue import PayloadQueue
import OPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.OUT)

wdstatus = True
stop = False

class ProcessMonitor ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    periodicTimerCount = 0

    modbusDataServiceCount = 0

    messageComposerCount = 0

    messageSenderCount = 0


    def __init__( self ):
        threading.Thread.__init__( self )

    def run( self ):
        global stop

        while True:
            if stop:
                self.LOG.info( 'Stop signal received from the main module. Going to stop thread.' )
                break
            try:
                time.sleep( 10 )
                self.LOG.info('Feeding watchdog')
                self.checkStatus()
                self.feedWatchdog()
            except Exception as e:
                self.LOG.error('Error in ProcessMonitor %s', e)

    ##
    #
    def feedWatchdog( self ):
        try:
            subprocess.call( 'sync', shell=True )
        except Exception as e:
            self.LOG.error( 'Error syncing filesystem changes: %s', e )

        try:
            subprocess.call( 'hwclock -f /dev/rtc1 -w', shell=True )
        except Exception as e:
            self.LOG.error( 'Error syncing filesystem changes: %s', e )
        try:
            #subprocess.call( 'echo 1 > /dev/watchdog', shell=True )
            global wdstatus
            pinstatus = GPIO.HIGH
            if( wdstatus ):
                wdstatus = False
                pinstatus = GPIO.HIGH
            elif not wdstatus:
                wdstatus = True
                pinstatus = GPIO.LOW
            GPIO.output(19, pinstatus)
        except Exception as e:
            self.LOG.error( 'Error Feeding the watchdog: %s', e )

    ##
    #
    def checkModbusDeviceStatus( self ):
        healthy = False
        for status in Status.modbusDevStatus:
            print('Modbus status ', status)
            if status < 150:
                healthy = True
                break
        print(healthy)
        if not healthy:
            self.LOG.error( "Modbus Devices not responding. Going to reboot " )

        return healthy

    ##
    #
    def checkThreadsHealth( self ):
        if Status.periodicTimerWorking:
            Status.periodicTimerWorking = False
            self.periodicTimerCount = 0
        else:
            self.periodicTimerCount += 1

        if Status.modbusDataServiceWorking:
            Status.modbusDataServiceWorking = False
            self.modbusDataServiceCount = 0
        else:
            self.modbusDataServiceCount += 1

        if Status.messageComposerWorking:
            Status.messageComposerWorking = False
            self.messageComposerCount = 0
        else:
            self.messageComposerCount += 1

        if Status.messageSenderWorking:
            Status.messageSenderWorking = False
            self.messageSenderCount = 0
        else:
            self.messageSenderCount += 1

        if self.periodicTimerCount > 90 or \
           self.modbusDataServiceCount > 90 or \
           self.messageComposerCount > 90 or \
           self.messageSenderCount > 90:
            return False
        else:
            return True


    ##
    #
    def checkStatus( self ):
        modbusDevStatus = self.checkModbusDeviceStatus()

        threadStatus = self.checkThreadsHealth()

        if not GsmUtility.internetPresent():
            LedStatus.led_status = LedStatus.LED_STABLE
        else:
            LedStatus.led_status = LedStatus.LED_OFF

        if not threadStatus and not Status.stop:
            self.LOG.error( "Thread status not updating. Going to reboot" )
            rebootPayload = '<GATEWAY_ID V=\''  + Status.deviceId +  '\'><REBOOT>APP NOT WORKING PROPERLY</REBOOT></GATEWAY_ID>'
            PayloadQueue().appendPayload(rebootPayload)
            Status.stop = True
            return

        if not modbusDevStatus and not Status.stop:
            pass
            #rebootPayload = '<GATEWAY_ID V=\''  + Status.deviceId +  '\'><REBOOT>MODBUS NOT RESPONDING</REBOOT></GATEWAY_ID>'
            #PayloadQueue().appendPayload(rebootPayload)
            #Status.stop = True
