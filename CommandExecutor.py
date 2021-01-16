#!/usr/bin/env python

##
#  @package CommsndExecutor Package contains the utility function for executing all the supported commands
#

from MainConfig import MainConfig
import logging
import subprocess
import simplejson as json
from ModbusDeviceList import ModbusDeviceList
import requests


LOG = logging.getLogger(__name__)

## Command IDs
CMD_REBOOT = 'REBOOT'
CMD_UPDATE_MAIN_CONFIG = 'UPDATE_MAIN_CONFIG'
CMD_REPLACE_MAIN_CONFIG = 'REPLACE_MAIN_CONFIG'
CMD_REPLACE_DEVICE_CONFIG = 'REPLACE_DEVICE_CONFIG'


def executeCommand( commandId, args ):
    if commandId == CMD_REBOOT:
        rebootDevice()
    elif commandId == CMD_UPDATE_MAIN_CONFIG:
        updateMainConfig( args )
    elif commandId == CMD_REPLACE_MAIN_CONFIG:
        replaceMainConfig( args )
    elif commandId == CMD_REPLACE_DEVICE_CONFIG:
        replaceDeviceConfig( args )
    else:
        LOG.warn( 'Unknown command: %s', commandId )


def executeSmsCommand( commandId, args ):
    pass


def updateMainConfig( args ):
    
    try:
        params = args.get('params')
        if params is not None:
            mc = MainConfig().getConfig()
            for key,value in params.items():
                mc[key] = value

            with open( MainConfig().CONFIG_PATH, 'w' ) as f:
                f.truncate()
                json.dump( mc, f, indent=4 )

            try:
                subprocess.call( 'sync', shell=True )
            except Exception as e:
                LOG.error( 'Error syncing filesystem changes: %s', e )

            rebootDevice()

    except Exception as e:
        LOG.error('Error updating main config: %s', e)


def replaceMainConfig( args ):
    try:
        newConfig = args.get('new_config')
        if newConfig is not None:
            with open( MainConfig().CONFIG_PATH, 'w' ) as f:
                f.truncate()
                json.dump( newConfig, f, indent=4 )
            try:
                subprocess.call( 'sync', shell=True )
            except Exception as e:
                LOG.error( 'Error syncing filesystem changes: %s', e )

            rebootDevice()

    except Exception as e:
        LOG.error('Error replacing the main config with new config: %s', e)


def replaceDeviceConfig( args ):
    try:
        newDeviceConfig = args.get('new_device_config')
        if newDeviceConfig is not None:
            with open( ModbusDeviceList().CONFIG_PATH, 'w' ) as f:
                f.truncate()
                json.dump( newDeviceConfig, f, indent=4 )
            try:
                subprocess.call( 'sync', shell=True )
            except Exception as e:
                LOG.error( 'Error syncing filesystem changes: %s', e )

            rebootDevice()

    except Exception as e:
        LOG.error('Error replacing the device config with new config: %s', e)


def rebootDevice():
    try:
        subprocess.call( 'reboot', shell=True )
    except Exception as e:
        LOG.error( 'Error syncing filesystem changes: %s', e )


def updateFirmwareArchive( args ):
    try:
        update_url = args.get('update_file')
        checksum_url = args.get('checksum')
        fw_version = args.get('fw_version')
        if update_url is None or checksum_url is None or fw_version is None:
            return
        
        try:
            subprocess.call('rm -rf /fw/update', shell=True)
            subprocess.call('mkdir /fw/update', shell=True)
        except:
            pass

        download_file(update_url, base_path='/fw/update')
        download_file(checksum_url, base_path='/fw/update')

        try:
            subprocess.call('sync', shell=True)
        except:
            pass

        with open('/fw/update/version', 'w') as f:
            f.write(fw_version) 

        rebootDevice()

    except Exception as e:
        LOG.error('Error updating firmware: %s', e)



def download_file(url, base_path='/fw/'):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename