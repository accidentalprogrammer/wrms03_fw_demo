#!/usr/bin/env python

# V1.1
##
#  This script contains the code to connect to the server and execute the commands received from the server
#
import requests
import simplejson as json
import subprocess
import OPi.GPIO as GPIO
import time
import subprocess
from MainConfig import MainConfig
from Constants import Constants

# Pin Definitons:
onPin = 16
pwrKey = 12
statusPin = 18


GPIO.setmode(GPIO.BOARD)
GPIO.setup(onPin, GPIO.OUT)
GPIO.setup(pwrKey, GPIO.OUT)
GPIO.setup(statusPin, GPIO.IN)

def resetModem():
    GPIO.output(onPin, GPIO.LOW) # set the GSM ON/OFF pin to low to turn off the modem
    time.sleep(10)
    GPIO.output(onPin, GPIO.HIGH) # set the GSM ON/OFF pin to high to turn on the modem
    time.sleep(5)
    # Then Toggle the power key
    GPIO.output(pwrKey, GPIO.HIGH)
    GPIO.output(pwrKey, GPIO.LOW)
    time.sleep(5)
    GPIO.output(pwrKey, GPIO.HIGH)
    time.sleep(30)
    status = GPIO.input(statusPin)
    try:
        if status == 1:
            subprocess.Popen(['wvdial -C /root/DataLogger/recovery/wvdial.conf'], shell=True)
    except Exception as e:
        print(e)
    time.sleep(5)
    print('GSM Status: ', GPIO.input(statusPin))



def processResponse( response ):
    respJson = {}

    try:
        respJson = json.loads( response )
    except Exception as e:
        self.LOG.error( "Error parsing response: %s", e )
        return

    if 'command_list' in respJson:
        commandList = respJson.get( 'command_list' )
        for command in commandList:
            try:
                print('Executing command: ',command)
                subprocess.call( command, shell=True )
            except Exception as e:
                print( 'Error executing command: ', command )


def internetPresent():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname('www.google.com')
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


def executeConnectServer():
    if not internetPresent():
        resetModem()

    result = False
    primaryUrl = 'http://13.235.41.207:9000/remoteCommand'
    secUrl = ''
    mc = MainConfig().getConfig()
    data = { 'imei': 'WBETESTGTWYIN0000' }
    try:
        headers = { 'Accept':'application/json','Content-Type': 'application/x-www-form-urlencoded' }
        response = requests.post( primaryUrl, data=data, headers=headers )
        resStatus = response.status_code
        if resStatus == 200:
            resbody = response.content.decode('utf-8')
            processResponse(resbody)
            result = True
        else:
            pass
    except Exception as e:
        print( 'Error sending payload: %s', e )
    finally:
        pass

    if not result:
        try:
            headers = { 'Accept':'application/json','Content-Type': 'application/x-www-form-urlencoded' }
            response = requests.post( secUrl, data=data, headers=headers )
            resStatus = response.status_code
            if resStatus == 200:
                resbody = response.content.decode('utf-8')
                processResponse(resbody)
                result = True
            else:
                pass
        except Exception as e:
            print( 'Error sending payload: %s', e )
        finally:
            pass

executeConnectServer()
