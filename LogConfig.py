#!/usr/bin/env python


##
#  @package LogConfig Module contains reads the logging configurations and stores in the variable
#

from os import listdir, path
import yaml

class LogConfig:

    class __LogConfig:
        def __init__( self ):
            pass

        ## Dictionary conataining the configuration
        config = {}

        ## Path where all Configuration file is stored
        CONFIG_PATH = '/fw/DataLogger/config/logging.yaml'


        ## Function to read the configuration
        #
        def readConfiguration( self ):
            with open( self.CONFIG_PATH, 'r' ) as f:
                self.config = yaml.safe_load(f.read())

        ## Function to return the logging configuration
        #  @return config dictionary: Dictionary containing the logging configuration
        #
        def getConfig( self ):
            return self.config

    ## Singleton instance of the private __LogConfig class
    instance = None

    def __init__( self ):
        if not LogConfig.instance:
            LogConfig.instance = LogConfig.__LogConfig()
            try:
                LogConfig.instance.readConfiguration()
            except Exception as e:
                print( "Error reading the logging configuration ",e)


    # TODO: Figure out why it doesn't work without name argument
    def __getattr__( self, name ):
        return getattr( self.instance, name )
