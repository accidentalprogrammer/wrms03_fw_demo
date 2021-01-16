#!/usr/bin/env python

##
#  @package ParamValueStore This package contains the class that reads and stores the parameters values
#  required for further calculation on the disk
#


import logging
from os import listdir, path
import simplejson as json


class ParamValueStore:

    LOG = logging.getLogger( __name__ )

    class __ParamValueStore:
        def __init__( self ):
            pass

        ## Path where the file containing the param values is stored on disk
        FILE_PATH = '/fw/DataLogger/logs/value_store.json'

        ## Dictionary containing the contents read from the file
        valueStore = {}

        ## Function to read the value file
        #
        def readParamValues( self ):
            with open( self.FILE_PATH ) as f:
                self.valueStore = json.load(f)

        ##
        #  Function to return the values dictionary
        #  @return config dictionary: Dictionary containing the stored values
        #
        def getValueStore( self ):
            return self.valueStore

        ##
        #  Function to store the values dictionary on the disk
        #
        def storeValues( self, vs ):
            try:
                with open( self.FILE_PATH, 'w' ) as f:
                    json.dump( vs, f, indent=4 )
            except Exception as e:
                pass

    ## Singleton instance of the private __ParamValueStore class
    instance = None

    def __init__( self ):
        if not ParamValueStore.instance:
            ParamValueStore.instance = ParamValueStore.__ParamValueStore()
            try:
                ParamValueStore.instance.readParamValues()
            except Exception as e:
                self.LOG.error( 'Error reading the main configuration: %s', e )


    # TODO: Figure out why it doesn't work without name argument
    def __getattr__( self, name ):
        return getattr( self.instance, name )
