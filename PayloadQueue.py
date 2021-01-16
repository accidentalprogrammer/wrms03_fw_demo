#!/usr/bin/env python

##
#  @package PayloadQueue Module contains the Logic to read write the data into the file containing the payload data
#


import logging
import time
import subprocess
import Status
import sqlite3

resourceBusy = False

class PayloadQueue:

    LOG = logging.getLogger( __name__ )


    PAYLOAD_FILE = '/fw/DataLogger/logs/upload_data.log'

    resourceBusy = False


    ##
    #
    def takePayloadFileLock( self ):
        global resourceBusy
        while( resourceBusy ):
            time.sleep( 0.1 )

        resourceBusy = True

        return True

    ##
    #
    def givePayloadFileLock( self ):
        global resourceBusy
        resourceBusy = False

    ##
    #  Function to append a single data at the end of the file
    def _appendPayloadFile( self, payload ):
        global resourceBusy
        while( resourceBusy ):
            time.sleep( 0.1 )

        resourceBusy = True

        try:
            with open( self.PAYLOAD_FILE, 'a+', errors="ignore" ) as pfile:
                pfile.write( payload + '\n' )
        except Exception as e:
            self.LOG.error( 'Error reading backlog file: %s', e)

        resourceBusy = False

    ##
    #  Function to check if there is backlog data present in the device
    #
    #  @return present boolean: returns true if backlog is present false otherwise
    #
    def _isBacklogPresentFile( self ):
        global resourceBusy
        while( resourceBusy ):
            time.sleep( 0.1 )

        resourceBusy = True

        present = False
        try:
            with open( self.PAYLOAD_FILE, 'r', errors="ignore" ) as pfile:
                line = pfile.readline()
                if line == '\n' or line == '':
                    present = False
                else:
                    present = True
        except Exception as e:
            self.LOG.error( 'Error reading backlog file: %s', e )

        resourceBusy = False

        return present


    ##
    #  Function to get the 
    def _getPayloadFile( self ):
        global resourceBusy
        while( resourceBusy ):
            time.sleep( 0.1 )

        resourceBusy = True
        payload = None

        try:
            with open( self.PAYLOAD_FILE, 'r+', errors="ignore") as pfile:
                payload = pfile.readline()
        except Exception as e:
            self.LOG.error( 'Error reading backlog file: %s', e )

        resourceBusy = False

        return payload


    ##
    #
    def _deleteLastPayloadFile( self ):
        global resourceBusy
        while( resourceBusy ):
            time.sleep( 0.1 )

        resourceBusy = True

        command1 = 'tail -n +2 ' + self.PAYLOAD_FILE + ' > ' + self.PAYLOAD_FILE + '.tmp'
        command2 = 'mv ' + self.PAYLOAD_FILE + '.tmp ' + self.PAYLOAD_FILE
        try:
            return_code = subprocess.call( command1, shell=True )
        except Exception as e:
            self.LOG.error( 'Error moving the payload file: %s', e )
        self.LOG.debug( 'Command1 return: %s',return_code )

        try:
            return_code = subprocess.call( command2, shell=True )
        except Exception as e:
            self.LOG.error( 'Error moving the payload file: %s', e )
        self.LOG.debug( 'Command2 return: %s',return_code )

        resourceBusy = False


    ##
    #
    def _appendPayloadSqlite( self, payload ):
        try:
            print('Appending to payload queue')
            print(payload)
            conn = sqlite3.connect('/fw/sqlite/payload.db')
            c = conn.cursor()
            c.execute("insert into backlog values ( ? )", (payload,))
            conn.commit()
            conn.close()
        except Exception as e:
            self.LOG.error('Error appending payload to backlog table %s', e)
    

    ##
    #
    def _isBacklogPresentSqlite( self ):
        try:
            conn = sqlite3.connect('/fw/sqlite/payload.db')
            c = conn.cursor()
            c.execute("SELECT COUNT(*) from backlog")
            countr = c.fetchone()
            count = int(countr[0])
            conn.commit()
            conn.close()
            print('Backlog count: ', count)
            present = True if count > 0 else False
            return present
        except Exception as e:
            self.LOG.error('Error checking for backlog: %s', e)


    ##
    #
    def _getPayloadSqlite( self ):
        try:
            conn = sqlite3.connect('/fw/sqlite/payload.db')
            c = conn.cursor()
            c.execute("SELECT * from backlog limit 1")
            payload = c.fetchone()[0]
            conn.commit()
            conn.close()
            return payload
        except Exception as e:
            self.LOG.error('Error fetchig backlog from sqlite: %s', e)
        
        return None


    ##
    #
    def _deleteLastPayloadSqlite( self ):
        try:
            conn = sqlite3.connect('/fw/sqlite/payload.db')
            c = conn.cursor()
            c.execute("SELECT MIN(rowid) from backlog")
            rowid = c.fetchone()[0]
            c.execute("DELETE FROM backlog where rowid =?", (rowid,))
            conn.commit()
            conn.close()
        except Exception as e:
            self.LOG('Error deleting the payload from sqlite: %s', e)

    ##
    # Wrapper function to append the new payload in the persistent storage
    def appendPayload( self, payload ):
        if int(Status.fwVersion) < 13:
            self._appendPayloadFile(payload)
        else:
            self._appendPayloadSqlite(payload)

    ##
    # Wrapper function to check if the backlog is present in the persistent storage
    def isBacklogPresent( self ):
        if int(Status.fwVersion) < 13:
            return self._isBacklogPresentFile()
        else:
            return self._isBacklogPresentSqlite()

    
    ##
    # Wrapper function to get the last payload from the persistent storage
    def getPayload( self ):
        if int(Status.fwVersion) < 13:
            return self._getPayloadFile()
        else:
            return self._getPayloadSqlite()

    ##
    # Wrapper function to delete the last payload from the persistent storage
    def deleteLastPayload( self ):
        if int(Status.fwVersion) < 13:
            self._deleteLastPayloadFile()
        else:
            self._deleteLastPayloadSqlite()



    ##
    #
    def deletePayloadFile( self ):
        global resourceBusy
        while( resourceBusy ):
            time.sleep( 0.1 )

        resourceBusy = True

        cmdDeletePayloadFile = 'rm ' + self.PAYLOAD_FILE
        try:
            subprocess.call( cmdDeletePayloadFile, shell=True )
        except Exception as e:
            self.LOG.error( 'Error deleting payload file: %s', e)
