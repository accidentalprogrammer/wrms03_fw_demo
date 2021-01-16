#!/usr/bin/env python

##
#  @package ModbusDeviceConfig Provide a singleton instance for accessing
#  modbus controller related configuration files
#

import logging
from os import listdir, path
import simplejson as json

class ModbusDeviceConfig:

#    LOG = logging.getLogger(__name__)

    class __ModbusDeviceConfig:
        def __init__( self ):
            pass

        ## Dictionary conataining all the configuration for the Modbus Devices
        config = {}

        ## Path where all Modbus Configuration files are stored
        CONFIG_PATH = '/fw/DataLogger/app/modbus_config/'

        ## Function to get the list of all the Modbus Configuration files
        #  @return fileList List: List containing names of all the configuration files
        #
        def getConfigFileList( self ):
            fileList = [ f for f in listdir( self.CONFIG_PATH ) if path.isfile( self.CONFIG_PATH+f )]
            return fileList

        ## Function to read all the Modbus configuration files present in the Modbus config path and sotre it in the instance variabe config
        #
        def readConfiguration( self ):
            fileList = self.getConfigFileList()
            for configFile in fileList:
                with open( self.CONFIG_PATH + configFile ) as f:
                    modbusConfig = json.load(f)
                    truncPoint = configFile.find( '.' ) if configFile.find( '.' ) > -1 else len( configFile )
                    configKey = configFile[:truncPoint].upper()
                    self.config[configKey] = modbusConfig


        ## Function to return the Modbus Device configuration of a particular device
        #  @param configKey string: The unique key to identify the configuration of the controller
        #  @return modbusConfig dictionary: Dictionary containing the Modbus device configuration or None if the configuration does not exist
        #
        def getModbusConfig( self, configKey ):
            return self.config.get( configKey.upper() )

    ## Singleton instance of the private __ModbusDeviceConfig class
    instance = None

    def __init__( self ):
        if not ModbusDeviceConfig.instance:
            ModbusDeviceConfig.instance = ModbusDeviceConfig.__ModbusDeviceConfig()
            ModbusDeviceConfig.instance.readConfiguration()

    # TODO: Figure out why it doesn't work without name argument
    def __getattr__( self, name ):
        return getattr( self.instance, name )
