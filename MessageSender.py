#!/usr/bin/env python


##
#  @package MessageSender Module contains the logic for sending the constructed payload to the server
#

import logging
import PeriodicTimer
import threading
import time
from PayloadQueue import PayloadQueue
from HttpSender import HttpSender
from MqttSender import MqttSender
import Status
import LedStatus
import GsmUtility


stop = False

class MessageSender ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    def __init__( self ):
        threading.Thread.__init__( self )

    ##
    #
    def run( self ):
        global stop
        while True:
            Status.messageSenderWorking = True
            if stop:
                self.LOG.info( 'Got stop signal from the Main module. Stopping thread' )
                break

            try:
                self.LOG.info('Sleeping for: %s', 30)
                time.sleep( 30 )

                if GsmUtility.internetPresent():
                    self.sendPayload()
                    try:
                        subprocess.call( 'sync', shell=True )
                    except Exception as e:
                        self.LOG.error( 'Error syncing filesystem changes: %s', e )
                self.sendPayload()
            except Exception as e:
                self.LOG.error( 'Error in Message Sender module: %s', e)


    ##
    #
    def sendPayload( self ):
        self.LOG.info( 'Sending Payload' )
        pq = PayloadQueue()
        print(pq.isBacklogPresent())
        while pq.isBacklogPresent():
            print('Backlog is present')
            payload = pq.getPayload()
            retries = 3
            sender = HttpSender()
            success = False
            while retries > 0:
                retries -= 1
                if sender.sendPayload( payload ):
                    pq.deleteLastPayload()
                    success = True
                    self.LOG.info( 'Payload sent' )
                    break
            if not success:
                self.LOG.warning( 'Payload sending failed' )
                break
