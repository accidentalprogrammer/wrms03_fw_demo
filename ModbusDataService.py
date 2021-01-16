#!/usr/bin/env python


##
#  @package ModbusDataAcquisitionService Service which runs in a seaparate thread
#  and queries all the Modbus Devices configured

import threading
from ModbusConsts import ModbusConsts
from ModbusDeviceList import ModbusDeviceList
from ModbusRtuAcquisition import ModbusRtuAcquisition
from ModbusDeviceConfig import ModbusDeviceConfig
import time
import logging
from SerialConnection import SerialConnection
from LoraConnection import LoraConnection
import InputDataQueue
from ModbusDecoder import ModbusDecoder
import PeriodicTimer
import Status
from ModbusSlaveCardAcquisition import ModbusSlaveCardAcquisition
from AlarmProcessor import AlarmProcessor


stop = False

class ModbusDataService ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    def __init__( self ):
        threading.Thread.__init__( self )

    def run( self ):
        global stop

        while(1):
            Status.modbusDataServiceWorking = True
            if stop:
                self.LOG.info( 'Got stop sigal from the main module. Going to stop thread' )
                break
            try:
                Status.modbuslock.acquire()
                self.queryModbusDevices()
                Status.modbuslock.release()
            except Exception as e:
                self.LOG.error( 'Error querying the Modbus devices: %s', e )

            time.sleep( PeriodicTimer.counter )

    ##
    #  Function to query all the configured Modbus devices
    def queryModbusDevices( self ):
        modbusDevList = ModbusDeviceList().getModbusDeviceList()
        modbusResponseList = []
        index = 0
        print('No of modbus devices: ', modbusDevList)
        for modbusDevice in modbusDevList:
            print('Modbus Device ', modbusDevice)
            ser = None
            try:
                print('here1')
                connectionType = modbusDevice.get( ModbusConsts.CONN_TYPE )
                if connectionType is None:
                    continue

                if connectionType == ModbusConsts.CONN_RTU:
                    print('here2')
                    connParams = modbusDevice.get( ModbusConsts.CONN_PARAMS )
                    print('here2.1')
                    modbusConfig = ModbusDeviceConfig().getModbusConfig( modbusDevice.get( ModbusConsts.DEVICE_TYPE ) )
                    print('here2.2')
                    self.LOG.debug(modbusConfig.get(ModbusConsts.QUERY_PARAMS))
                    print('here2.3')
                    try:
                        print('here3')
                        ser = SerialConnection().getSerialConnection( connParams.get( ModbusConsts.BAUDRATE ) ,
                                                                      connParams.get( ModbusConsts.PARITY ),
                                                                      connParams.get( ModbusConsts.STOP_BITS ),
                                                                      connParams.get( ModbusConsts.BYTE_SIZE ))
                    except Exception as e3:
                        self.LOG.error( 'Error Getting Serial connection: %s', e3 )

                    modbusResp = ModbusRtuAcquisition().queryDevice( int(connParams.get( ModbusConsts.SLAVE_ID )),
                                                                     ser,
                                                                     modbusConfig.get( ModbusConsts.QUERY_PARAMS ),
                                                                     index,
                                                                     connectionType
                    )
                    print('here4')
                    modbusResp[ModbusConsts.DEVICE_TYPE] = modbusDevice.get( ModbusConsts.DEVICE_TYPE )
                    modbusResp[ModbusConsts.SLAVE_ID] = connParams.get( ModbusConsts.SLAVE_ID )
                    modbusResp[ModbusConsts.DEVICE_CATEGORY] = modbusDevice.get( ModbusConsts.DEVICE_CATEGORY )
                    modbusResp[ModbusConsts.DEVICE_ID] = modbusDevice.get( ModbusConsts.DEVICE_ID )
                    if modbusDevice.get( ModbusConsts.TCS_DATA ) is not None:
                        modbusResp[ModbusConsts.TCS_DATA] = modbusDevice.get( ModbusConsts.TCS_DATA )

                    modbusResponseList.append( modbusResp )

                elif connectionType == ModbusConsts.CONN_TCP:
                    pass
                elif connectionType == ModbusConsts.CONN_RTU_TCP:
                    pass
                elif connectionType == ModbusConsts.CONN_RTU_LORA:
                    connParams = modbusDevice.get( ModbusConsts.CONN_PARAMS )
                    modbusConfig = ModbusDeviceConfig().getModbusConfig( modbusDevice.get( ModbusConsts.DEVICE_TYPE ) )
                    self.LOG.debug(modbusConfig.get(ModbusConsts.QUERY_PARAMS))
                    try:
                        ser = LoraConnection().getLoraConnection( connParams.get( ModbusConsts.BAUDRATE ),
                                                                  connParams.get( ModbusConsts.PARITY ),
                                                                  connParams.get( ModbusConsts.STOP_BITS ),
                                                                  connParams.get( ModbusConsts.BYTE_SIZE ))
                    except Exception as e3:
                        self.LOG.error( 'Error Getting LoRa Serial connection: %s', e3 )
                    modbusResp = ModbusRtuAcquisition().queryDevice( int(connParams.get( ModbusConsts.SLAVE_ID )),
                                                                     ser,
                                                                     modbusConfig.get( ModbusConsts.QUERY_PARAMS ),
                                                                     index
                    )

                    modbusResp[ModbusConsts.DEVICE_TYPE] = modbusDevice.get( ModbusConsts.DEVICE_TYPE )
                    modbusResp[ModbusConsts.SLAVE_ID] = connParams.get( ModbusConsts.SLAVE_ID )
                    modbusResp[ModbusConsts.DEVICE_CATEGORY] = modbusDevice.get( ModbusConsts.DEVICE_CATEGORY )
                    modbusResp[ModbusConsts.DEVICE_ID] = modbusDevice.get( ModbusConsts.DEVICE_ID )
                    if modbusDevice.get( ModbusConsts.TCS_DATA ) is not None:
                        modbusResp[ModbusConsts.TCS_DATA] = modbusDevice.get( ModbusConsts.TCS_DATA )

                    modbusResponseList.append( modbusResp )
                elif connectionType == ModbusConsts.CONN_TYPE_SLAVE_RS485:
                    connParams = modbusDevice.get( ModbusConsts.CONN_PARAMS )
                    try:
                        ser = SerialConnection().getSerialConnection( connParams.get( ModbusConsts.BAUDRATE ),
                                                                      connParams.get( ModbusConsts.PARITY ),
                                                                      connParams.get( ModbusConsts.STOP_BITS ),
                                                                      connParams.get( ModbusConsts.BYTE_SIZE ))
                    except Exception as e3:
                        self.LOG.error( 'Error Getting Serial connection: %s', e3 )
                    try:
                        modbusResp = ModbusSlaveCardAcquisition().querySlaveCard( modbusDevice, ser, index )
                        modbusResp[ModbusConsts.DEVICE_TYPE] = modbusDevice.get( ModbusConsts.DEVICE_TYPE )
                        modbusResp[ModbusConsts.SLAVE_ID] = connParams.get( ModbusConsts.SLAVE_ID )
                        modbusResp[ModbusConsts.DEVICE_CATEGORY] = modbusDevice.get( ModbusConsts.DEVICE_CATEGORY )
                        modbusResp[ModbusConsts.DEVICE_ID] = modbusDevice.get( ModbusConsts.DEVICE_ID )
                        modbusResponseList.append( modbusResp )
                    except Exception as e:
                        print(e)

                elif connectionType == ModbusConsts.CONN_TYPE_SLAVE_LORA:
                    print('Querying Lora Slave')
                    connParams = modbusDevice.get( ModbusConsts.CONN_PARAMS )
                    try:
                        ser = LoraConnection().getLoraConnection( connParams.get( ModbusConsts.BAUDRATE ),
                                                                  connParams.get( ModbusConsts.PARITY ),
                                                                  connParams.get( ModbusConsts.STOP_BITS ),
                                                                  connParams.get( ModbusConsts.BYTE_SIZE ))
                    except Exception as e3:
                        self.LOG.error( 'Error Getting LoRa Serial connection: %s', e3 )
                    modbusResp = ModbusSlaveCardAcquisition().querySlaveCard( modbusDevice, ser, index )
                    modbusResp[ModbusConsts.DEVICE_TYPE] = modbusDevice.get( ModbusConsts.DEVICE_TYPE )
                    modbusResp[ModbusConsts.SLAVE_ID] = connParams.get( ModbusConsts.SLAVE_ID )
                    modbusResp[ModbusConsts.DEVICE_CATEGORY] = modbusDevice.get( ModbusConsts.DEVICE_CATEGORY )
                    modbusResp[ModbusConsts.DEVICE_ID] = modbusDevice.get( ModbusConsts.DEVICE_ID )
                    modbusResponseList.append(modbusResp)
                else:
                    self.LOG.warn( 'Connection Type not supported: %s', connectionType )

            except Exception as e2:
                self.LOG.error( 'Error querying the Modbus device: %s', e2 )
            index += 1
        mDecoder = ModbusDecoder()
        decodedData = mDecoder.decodeModbusData( modbusResponseList )
        print("Decoded Data: ",decodedData)
        try:
            decodedData = AlarmProcessor().processAlarms( decodedData, modbusDevice.get( ModbusConsts.DEVICE_TYPE ) )
        except Exception as e:
            self.LOG.error( 'Error processing alarms: %s', e )

        InputDataQueue.modbusDataQueue.put_nowait( decodedData )

    def writeUpsCommand( decodedData ):
        for devData in decodedData:
            if devData.get('device_type') == 'CON_WBE_UPS':
                try:
                    data = devData.get('data')
                    batVolt = int(data.get('PARAM_2'))
                    print(batVolt)
                    if batVolt <= 7500:
                        self.shutDownDevice()
                except Exception as e:
                    print('Error writing to UPS ', e)
    
    def shutDownDevice():
        try:
            ser = SerialConnection().getSerialConnection( '9600' ,
                                                          'none',
                                                          '1',
                                                          '8')
            command = 'FA1000060001020001'
            crc = ModbusLib.get_modbus_crc( bytearray.fromhex( command ) )
            command = command+crc
            print('UPS command', command)
            commandResp = ModbusCommandSender().sendCommand( ser, command, 'RTU' )
            if commandResp:
                print('UPS written successfully')
            else:
                print('Error  writing to UPS')
            try:
                subprocess.call( 'shutdown now', shell=True )
            except Exception as e:
                self.LOG.error( 'Error shutting down: %s', e )
        except Exception as e:
            print('Error writing to UPS', e)

    ##
    #
    def populateTcsSpecificData( self, modbusResp, tcsData ):
        if modbusResp is None or tcsData is None:
            return modbusResp

        modbusResp[ ModbusConsts.TCS_VERSION ] = tcsData.get( ModbusConsts.TCS_VERSION )
        modbusResp[ ModbusConsts.TCS_COORD_ALTITUDE ] = tcsData.get( ModbusConsts.TCS_COORD_ALTITUDE )
        modbusResp[ ModbusConsts.TCS_COORD_LATITUDE ] = tcsData.get( ModbusConsts.TCS_COORD_LATITUDE )
        modbusResp[ ModbusConsts.TCS_COORD_LONGITUDE ] = tcsData.get( ModbusConsts.TCS_COORD_LONGITUDE )
        modbusResp[ ModbusConsts.TCS_GEO_TYPE ] = tcsData.get( ModbusConsts.TCS_GEO_TYPE )
        modbusResp[ ModbusConsts.TCS_LINK_TYPE ] = tcsData.get( ModbusConsts.TCS_LINK_TYPE )
        modbusResp[ ModbusConsts.TCS_OBS_FEATURE ] = tcsData.get( ModbusConsts.TCS_OBS_FEATURE )
        modbusResp[ ModbusConsts.TCS_OBS_SENSOR ] = tcsData.get( ModbusConsts.TCS_OBS_SENSOR )
        modbusResp[ ModbusConsts.TCS_OFFERING ] = tcsData.get( ModbusConsts.TCS_OFFERING )
        modbusResp[ ModbusConsts.TCS_SERVICE ] = tcsData.get( ModbusConsts.TCS_SERVICE )

        return modbusResp
