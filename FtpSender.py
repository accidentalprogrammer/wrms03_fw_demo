#!/usr/bin/env python

##
#  @package FtpSender package contains the functionality to send upload the payload file to a server
#

import logging
import ftplib
from Constants import Constants
import PeriodicTimer
import subprocess



class FtpSender:

    LOG = logging.getLogger( __name__ )

    def sendPayload( self, payload ):

        result = False        
        try:
            mc = MainConfig().getConfig()
            gatewayId = mc.get( Constants.GATEWAY_ID )
            server = mc.get( Constants.FTP_URL )
            username = mc.get( Constants.FTP_USER )
            password = mc.get( Constants.FTP_PWD )
            recordTime = PeriodicTimer.recordTimestamp
            ftp_connection = ftplib.FTP(server, username, password)
            if Constants.FTP_DIR in mc:
                ftpDir = mc.get( Constants.FTP_DIR )
                ftp_connection.cwd( ftpDir )

            file_name = f'{gatewayId}_{recordTime}.csv'
            with open(f'/fw/DataLogger/logs/{file_name}', 'w') as f:
                f.write(payload)
            
            with open(f'/fw/DataLogger/logs/{file_name}', 'rb') as f:
                ftp_connection.storbinary(f'STOR {file_name}', f)

            try:
                subprocess.call( f'rm /fw/DataLogger/logs/{file_name}', shell=True )
            except Exception as e:
                self.LOG.error( 'Error deleting file: %s', e )

            result = True
        except Exception as e:
            LOG.error('Error sending payload: %s', e)

        return result
