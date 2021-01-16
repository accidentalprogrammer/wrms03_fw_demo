#!/usr/bin/env python


##
#  @package UpgradeFw Module contains the logic to upgrade the firmware
#

import subprocess
import pexpect
import sys
import time
from MainConfig import MainConfig
from Constants import Constants
import simplejson as json
import requests
from ModbusDeviceList import ModbusDeviceList
import urllib.parse
import logging

LOG = logging.getLogger( __name__ )

##
#
def getUrlEncodedGitUrl( url, user, pwd ):
    idx = -1
    try:
        idx = url.index(':')
    except Exception as e:
        pass

    if idx > 0:
        url = url[idx+3:]

    finalUrl = 'https://' + urllib.parse.quote( user ) + ':' + urllib.parse.quote( pwd ) + '@' + url

    return finalUrl


##
#
def updateFirmware():
    mc = MainConfig().getConfig()
    print(mc)
    repo_fix = mc.get( Constants.FW_REPO_FIX )
    success = False

    if repo_fix is not None:
        url = repo_fix.get( Constants.CONFIG_REPO_URL )
        user = repo_fix.get( Constants.REPO_USER )
        pwd = repo_fix.get( Constants.REPO_PWD )

        try:
            res = subprocess.call( 'rm -rf /root/fwupg', shell=True)
        except Exception as e:
            LOG.error( 'Error deleting upgrade directory %s', e )

        try:
            checkoutUrl = getUrlEncodedGitUrl( url, user, pwd )
            command = 'git clone ' + checkoutUrl + ' /root/fwupg'
            res = subprocess.call( command, shell=True )
            if res != 0:
                success = False
            else:
                success = True
                try:
                    with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                        fp.truncate( 0 )
                        fp.write( 'FW_UPDATE_REPO' )
                except Exception as e:
                    LOG.error( 'Error writing FW update status: %s', e )
        except Exception as e:
            LOG.error( 'Unable to update firmware via primary repo: %s', e )

    if not success:
        repo = mc.get( Constants.FW_REPO )
        if repo is not None:
            url = repo.get( Constants.CONFIG_REPO_URL )
            user = repo.get( Constants.REPO_USER )
            pwd = repo.get( Constants.REPO_PWD )

            try:
                res = subprocess.call( 'rm -rf /root/fwupg', shell=True)
            except Exception as e:
                LOG.error('Error deleting upgrade directory %s', e )

            try:
                checkoutUrl = getUrlEncodedGitUrl( url, user, pwd )
                command = 'git clone ' + checkoutUrl + ' /root/fwupg'
                res = subprocess.call( command, shell=True )
                if res != 0:
                    success = False
                else:
                    success = True
                    try:
                        with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                            fp.truncate( 0 )
                            fp.write( 'FW_UPDATE_REPO' )
                    except Exception as e:
                        LOG.warning( 'Error writing update status: %s', e )
            except Exception as e:
                LOG.error( 'Unable to update firmware via secondary repo: %s', e )

    if not success:
        mc = MainConfig().getConfig()
        url = mc.get( Constants.FW_SERVER_URL_FIX )
        try:
            command = 'rm /root/GATEWAY.zip'
            res = subprocess.call( command, shell=True )
        except Exception as e:
            LOG.error( 'Unable to remove old update archive: %s', e )

        try:
            command = 'wget '+ url + ' -P /root'
            res = subprocess.call( command, shell=True )
            if res != 0:
                success = False
            else:
                success = True
                try:
                    with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                        fp.truncate( 0 )
                        fp.write( 'FW_UPDATE_ARCHIVE' )
                except Exception as e:
                    LOG.warning( 'Error writing update status: %s', e )
        except Exception as e:
            LOG.error( 'Unable to download the update archive fromt the first server URL: %s', e )

    if not success:
        mc = MainConfig().getConfig()
        url = mc.get( Constants.FW_SERVER_URL )
        try:
            command = 'rm /root/GATEWAY.zip'
            res = subprocess.call( command, shell=True )
        except Exception as e:
            LOG.error( 'Unable to remove old update archive: %s', e )

        try:
            command = 'wget '+ url + ' -P /root'
            res = subprocess.call( command, shell=True )
            if res != 0:
                success = False
            else:
                success = True
                try:
                    with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                        fp.truncate( 0 )
                        fp.write( 'FW_UPDATE_ARCHIVE' )
                except Exception as e:
                    LOG.warning( 'Error writing update status: %s', e )
        except Exception as e:
            LOG.error( 'Unable to download the update archive from the secondary server URL: %s', e )


    return success


##
#
def upgradeRepo( repo, user, pwd ):
    ret = False
    try:
        res = subprocess.call( 'rm -rf /root/fwupg', shell=True)
    except Exception as e:
        LOG.error("Error deleting upgrade directory %s", e )

    try:
        checkoutUrl = getUrlEncodedGitUrl( repo, user, pwd )
        command = 'git clone ' + checkoutUrl + '/root/fwupg'
        res = subprocess.call( command, shell=True )
        if res != 0:
            return False
        else:
            return True
    except Exception as e:
        LOG.error('Firmware update from first repo failed: %s', e )

    return ret

##
#
def upgradeArchive():

    mc = MainConfig().getConfig()
    url = mc.get( Constants.FW_SERVER_URL_FIX )
    try:
        command = 'rm /root/GATEWAY.zip'
        res = subprocess.call( command, shell=True )
    except Exception as e:
        LOG.error( 'Unable to remove old update archive: %s', e )

    try:
        command = 'wget '+ url + ' -P /root'
        res = subprocess.call( command, shell=True )
        if res != 0:
            return False
        else:
            return True
    except Exception as e:
        LOG.error( 'Unable to download the update archive fromt the first server URL: %s', e )


##
#
def upgradeApt():
    ret = False

    return ret



##
#
def updateModbusConfig():
    mc = MainConfig().getConfig()
    print(mc)
    repo_fix = mc.get( Constants.CONFIG_REPO_FIX )
    success = False

    if repo_fix is not None:
        url = repo_fix.get( Constants.CONFIG_REPO_URL )
        user = repo_fix.get( Constants.REPO_USER )
        pwd = repo_fix.get( Constants.REPO_PWD )

        try:
            res = subprocess.call( 'rm -rf /root/ModbusConfigUpdate', shell=True)
        except Exception as e:
            LOG.error( 'Error deleting upgrade directory %s', e )

        try:
            checkoutUrl = getUrlEncodedGitUrl( url, user, pwd )
            command = 'git clone ' + checkoutUrl + ' /root/ModbusConfigUpdate'
            res = subprocess.call( command, shell=True )
            if res != 0:
                success = False
            else:
                success = True
                try:
                    with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                        fp.truncate( 0 )
                        fp.write( 'MODBUS_CONFIG_UPDATE' )
                except Exception as e:
                    LOG.error( 'Error writing Modbus config update status: %s', e )
        except Exception as e:
            LOG.error( 'Unable to update modbus device config via primary repo: %s', e )

    if not success:
        repo = mc.get( Constants.CONFIG_REPO_SEC )
        if repo is not None:
            url = repo.get( Constants.CONFIG_REPO_URL )
            user = repo.get( Constants.REPO_USER )
            pwd = repo.get( Constants.REPO_PWD )

            try:
                res = subprocess.call( 'rm -rf /root/ModbusConfigUpdate', shell=True)
            except Exception as e:
                LOG.error('Error deleting upgrade directory %s', e )

            try:
                checkoutUrl = getUrlEncodedGitUrl( url, user, pwd )
                command = 'git clone ' + checkoutUrl + ' /root/ModbusConfigUpdate'
                res = subprocess.call( command, shell=True )
                if res != 0:
                    success = False
                else:
                    success = True
                    try:
                        with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                            fp.truncate( 0 )
                            fp.write( 'MODBUS_CONFIG_UPDATE' )
                    except Exception as e:
                        LOG.warning( 'Error writing Modbus config update status: %s', e )
            except Exception as e:
                LOG.error( 'Unable to update modbus device config via secondary repo: %s', e )

    if not success:
        url = mc.get( Constants.MODBUS_CONFIG_URL_FIX )
        print(url)
        resp = None
        try:
            headers = {'Accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}
            resp = requests.get( url=url, headers=headers )
        except Exception as e:
            LOG.error( 'Error requesting Modbus config primary url: %s', e )

        respDict = None

        try:
            respDict = json.loads( resp.content )
            print(respDict)
        except Exception as e:
            LOG.error( 'Error parsing JSON: %s', e )

        if respDict is not None:
            try:
                with open( ModbusDeviceList().CONFIG_PATH, 'w' ) as f:
                    f.truncate()
                    json.dump( respDict, f, indent=4 )
                    success = True
            except Exception as e:
                LOG.error( 'Error updating modbus device config with primary server url: %s', e )

    if not success:
        url = mc.get( Constants.MODBUS_CONFIG_URL )
        print(url)
        resp = None
        try:
            headers = {'Accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}
            resp = requests.get( url=url, headers=headers)
        except Exception as e:
            LOG.error( 'Error requesting Modbus config secondary url: %s', e )

        respDict = None

        try:
            respDict = json.loads( resp.content )
            print(respDict)
        except Exception as e:
            LOG.error( 'Error parsing JSON: %s', e )

        if respDict is not None:
            try:
                with open( ModbusDeviceList().CONFIG_PATH, 'w' ) as f:
                    f.truncate()
                    json.dump( respDict, f, indent=4 )
                    success = True
            except Exception as e:
                LOG.error( 'Error updating modbus device config with secondary server url: %s', e )

    return success

##
#
def updateMainConfig():
    mc = MainConfig().getConfig()
    repo_fix = mc.get( Constants.CONFIG_REPO_FIX )
    success = False

    if repo_fix is not None:
        url = repo_fix.get( Constants.CONFIG_REPO_URL )
        user = repo_fix.get( Constants.REPO_USER )
        pwd = repo_fix.get( Constants.REPO_PWD )

        try:
            res = subprocess.call( 'rm -rf /root/MainConfigUpdate', shell=True)
        except Exception as e:
            LOG.error('Error deleting upgrade directory %s', e )

        try:
            checkoutUrl = getUrlEncodedGitUrl( url, user, pwd )
            command = 'git clone ' + checkoutUrl + ' /root/MainConfigUpdate'
            res = subprocess.call( command, shell=True )
            if res != 0:
                success = False
            else:
                success = True
                try:
                    with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                        fp.truncate( 0 )
                        fp.write( 'MAIN_CONFIG_UPDATE' )
                except Exception as e:
                    LOG.error( 'Error Writing Main config update status: %s', e )
        except Exception as e:
            LOG.error( 'Error updating main config via primary repo: %s', e )

    if not success:
        repo = mc.get( Constants.CONFIG_REPO_SEC )
        if repo is not None:
            url = repo.get( Constants.CONFIG_REPO_URL )
            user = repo.get( Constants.REPO_USER )
            pwd = repo.get( Constants.REPO_PWD )

            try:
                res = subprocess.call( 'rm -rf /root/MainConfigUpdate', shell=True)
            except Exception as e:
                LOG.error('Error deleting upgrade directory %s', e )

            try:
                checkoutUrl = getUrlEncodedGitUrl( url, user, pwd )
                command = 'git clone ' + checkoutUrl + ' /root/MainConfigUpdate'
                res = subprocess.call( command, shell=True )
                if res != 0:
                    success = False
                else:
                    success = True
                    try:
                        with open( Constants.FW_UPG_INFO_FILE, 'w' ) as fp:
                            fp.truncate( 0 )
                            fp.write( 'MAIN_CONFIG_UPDATE' )
                    except Exception as e:
                        LOG.error( 'Error Writing Main config update status: %s', e )
            except Exception as e:
                LOG.error( 'Error updating main config via secondary repo: %s', e )

    if not success:
        url = mc.get( Constants.MAIN_CONFIG_URL_FIX )
        resp = None
        try:
            headers = {'Accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}
            resp = requests.get( url=url, headers=headers )
        except Exception as e:
            LOG.error( 'Error requesting Modbus config from primary url: %s', e )

        respDict = None

        try:
            respDict = json.loads( resp.content )
        except Exception as e:
            LOG.error( 'Error parsing JSON: %s', e )

        if respDict is not None:
            try:
                with open( MainConfig().CONFIG_PATH, 'r' ) as f:
                    currentConfig = json.load(f)
            except Exception as e:
                LOG.error( 'Error Loading current config: %s', e )

            for key, value in respDict.items():
                if value != 'Null':
                    currentConfig[key] = value

            try:
                with open( MainConfig().CONFIG_PATH, 'w' ) as f:
                    json.dump( currentConfig, f, indent=4 )
                    success = True
                    LOG.info('Main config update successful with main_config_url_fix')
            except Exception as e:
                LOG.error( 'Error writing main config: %s', e )

    if not success:
        url = mc.get( Constants.MAIN_CONFIG_URL )
        resp = None
        try:
            headers = {'Accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}
            resp = requests.get( url=url, headers=headers)
        except Exception as e:
            LOG.error( 'Error requesting Modbus config fix url: %s', e )

        respDict = None

        try:
            respDict = json.loads( resp.content )
        except Exception as e:
            LOG.error( 'Error parsing JSON: %s', e )

        if respDict is not None:
            try:
                with open( MainConfig().CONFIG_PATH, 'r' ) as f:
                    currentConfig = json.load(f)
            except Exception as e:
                LOG.error( 'Error Loading current config: %s', e )

            for key, value in respDict.items():
                if value != 'Null':
                    currentConfig[key] = value

            try:
                with open( MainConfig().CONFIG_PATH, 'w' ) as f:
                    json.dump( currentConfig, f, indent=4 )
                    success = True
            except Exception as e:
                LOG.error( 'Error writing main config: %s', e )

    return success

