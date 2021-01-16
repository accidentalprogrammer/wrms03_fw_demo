#!/usr/bin/env python


##
#  @package PeriodicTimer Module contains the periodic timer to synchronize all the tasks
#

import threading
import logging
from MainConfig import MainConfig
from Constants import Constants
import Status
import datetime
import time
import logging.config
from LogConfig import LogConfig

counter = 0
payloadCount = 0
recordTimestamp = None

stop = False


class PeriodicTimer ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    def __init__( self ):
        threading.Thread.__init__( self )

    def run( self ):
        self.LOG.debug('PeriodicTimer statrted')
        global counter
        global recordTimestamp
        mc = MainConfig().getConfig()
        recordTimestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        counter = 60 if mc.get( Constants.PERIODIC_INTERVAL ) is None else int(mc.get( Constants.PERIODIC_INTERVAL ))
        print("Periodic Interval: ",counter)
        self.increment()


    ##
    #  Function to reload and decrement periodic counter
    def increment( self ):
        Status.periodicTimerWorking = True
        global counter
        global payloadCount
        global stop
        global recordTimestamp
        if not stop:
            threading.Timer( 1.0, self.increment ).start()
        mc = MainConfig().getConfig()
        interval = 60 if mc.get( Constants.PERIODIC_INTERVAL ) is None else int(mc.get( Constants.PERIODIC_INTERVAL ))
        if time.time() % interval == 0 or time.time() % interval < 1:
            recordTimestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        counter -= 1
        if counter <= 1:
            print(recordTimestamp)
            counter = interval
            payloadCount += 1
