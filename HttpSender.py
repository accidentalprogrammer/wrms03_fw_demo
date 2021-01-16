#!/usr/bin/env python


##
#  @package HttpSender Module contains the functionality to send the message via HTTP
#

import logging
import http.client
from MainConfig import MainConfig
from Constants import Constants
import requests
import simplejson as json
import Status
import UpgradeFw
import GsmUtility
from LogConfig import LogConfig
import subprocess
import CommandExecutor as ce


class HttpSender:

    logging.config.dictConfig( LogConfig().getConfig() )
    LOG = logging.getLogger( __name__ )

    ##
    #
    def sendPayload( self, payload ):

        result = False
        try:
            mc = MainConfig().getConfig()
            url = mc.get( Constants.SERVER_HTTP_URL )
            headers = { 'Accept':'application/json','Content-Type': 'application/x-www-form-urlencoded' }
            data = { 'body':payload, 'deviceId': Status.deviceId, 'fwVersion': Status.fwVersion  }
            print('data: ', data)
            response = requests.post( url, data=data, headers=headers, timeout=15 )
            resStatus = response.status_code
            if resStatus == 200:
                Status.messageSendingFailedCount = 0
                resbody = response.content.decode('utf-8')
                print(resbody)
                self.processResponse( resbody )
                result = True
            else:
                Status.messageSendingFailedCount += 1
        except Exception as e:
            self.LOG.error( 'Error sending payload: %s', e )
            Status.messageSendingFailedCount += 1
        finally:
            pass

        return result

    ##
    #
    def processResponse( self, response ):
        respJson = {}

        try:
            respJson = json.loads( response )
        except Exception as e:
            self.LOG.error( "Error parsing response: %s", e )
            return

        if 'command_id' in respJson and 'args' in respJson:
            commandId = respJson.get('command_id')
            args = respJson.get('args')
            ce.executeCommand( commandId, args )


    def processCommands( self, commandList ):

        for command in commandList:
            try:
                print('Executing command: ',command)
                subprocess.call( command, shell=True )
            except Exception as e:
                self.LOG.error( 'Error executing command: %s', command )
                self.LOG.error('Error in executinf command: %s', e)



    ##
    #
    def doGetRequest( self, url, requestParams ):
        resp = None
        if requestParams is None:
            resp = requests.get( url=url)
        else:
            reap = requests.get( url=url, params=requestParams )
        return resp
