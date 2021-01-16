#!/usr/bin/env python

##
# @package JobDistributor Module contains the logic which distributes the data collection jobs among the different
# data collector threads at the right interval.


import threading
import logging
import time


stop = False

class JobDistributor ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    def __init__( self ):
        threading.Thread.__init__( self )

    def run( self ):
        global stop

        while True:
            if stop:
                self.LOG.info( 'Stop signal received from the main module. Going to stop thread.' )
                break
            try:
                
                time.sleep( 1 )
            except Exception as e:
                self.LOG.error('Error in JobDistributor %s', e)