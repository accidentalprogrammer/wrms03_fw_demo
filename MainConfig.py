#!/usr/bin/env python

##
#  @package MainConfig Module contains the Singleton implementation for the Main firmware configuration
#


import logging
from os import listdir, path
import simplejson as json

class MainConfig:

    LOG = logging.getLogger(__name__)

    class __MainConfig:
        def __init__( self ):
            pass

        ## Dictionary conataining the configuration
        config = {}

        ## Path where all Configuration file is stored
        CONFIG_PATH = '/fw/DataLogger/config/config.json'


        ## Function to read the configuration
        #
        def readConfiguration( self ):
            with open( self.CONFIG_PATH ) as f:
                self.config = json.load(f)

        ## Function to return the configuration
        #  @return config dictionary: Dictionary containing the configuration
        #
        def getConfig( self ):
            return self.config

    ## Singleton instance of the private __MainConfig class
    instance = None

    def __init__( self ):
        if not MainConfig.instance:
            MainConfig.instance = MainConfig.__MainConfig()
            try:
                MainConfig.instance.readConfiguration()
            except Exception as e:
                self.LOG.error( 'Error reading the main configuration: %s', e )


    # TODO: Figure out why it doesn't work without name argument
    def __getattr__( self, name ):
        return getattr( self.instance, name )
