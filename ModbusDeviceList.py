#!/usr/bin/env python


##
#  @package ModbusDeviceList Package containing the list of configured Modbus devices
#
import logging
from os import listdir, path
import simplejson as json

class ModbusDeviceList:
    LOG = logging.getLogger(__name__)

    class __ModbusDeviceList:
        def __init__( self ):
            pass

        ## Dictionary conataining all the configuration for the Modbus Devices
        config = []

        ## Path where all Modbus Configuration files are stored
        CONFIG_PATH = '/fw/DataLogger/modbus_dev/devices.json'


        ## Function to read all the Modbus configuration files present in the Modbus config path and store it in the instance variabe config
        #
        def readConfiguration( self ):
            try:
                with open( self.CONFIG_PATH ) as f:
                    modbusConfig = json.load(f)
                    self.config =  modbusConfig
            except Exception as e:
                print( "Error retreiving modbus devices: %s", e )


        ## Function to return the Modbus Device configuration of a particular device
        #  @return config List: List containing all the configured Modbus devices
        #
        def getModbusDeviceList( self ):
            return self.config

    ## Singleton instance of the private __ModbusDeviceList class
    instance = None

    def __init__( self ):
        if not ModbusDeviceList.instance:
            ModbusDeviceList.instance = ModbusDeviceList.__ModbusDeviceList()
            ModbusDeviceList.instance.readConfiguration()

    # TODO: Figure out why it doesn't work without name argument
    def __getattr__( self, name ):
        return getattr( self.instance, name )
