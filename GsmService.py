import time
import logging
import socket
import requests
import subprocess
import OPi.GPIO as GPIO


LOG = logging.getLogger( __name__ )

# Pin Definitons:
onPin = 16
pwrKey = 12
statusPin = 18

gsmConf = {}

def readConfiguration():
    try:
        with open('/fw/DataLogger/config/gsm.conf', 'r') as conf:
            for line in conf:
                line = line.strip()
                try:
                    pair = line.split('=')
                    key = pair[0]
                    value = pair[1]
                    gsmConf[key] = value
                except Exception as e:
                    LOG.error('Error reading configuration property : %s',e)
    except Exception as e2:
        LOG.error('Error reading GSM configuration : %s', e2)



def setupPins():
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(onPin, GPIO.OUT)
        GPIO.setup(pwrKey, GPIO.OUT)
        GPIO.setup(statusPin, GPIO.IN)
    except Exception as e:
        LOG.error('Error setting up the GSM PINs : %s', e)

##
#
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
    dns = '8.8.8.8' if gsmConf.get('DNS') is None else gsmConf.get('DNS')
    apn = 'airtelgprs.com' if gsmConf.get('APN') is None else gsmConf.get('APN')
    apnUser = 'user' if gsmConf.get('APN_USER') is None else gsmConf.get('APN_USER')
    apnPass = 'pass' if gsmConf.get('APN_PASS') is None else gsmConf.get('APN_PASS')
    usbInterface = '3' if gsmConf.get('USBINTERFACE') is None else gsmConf.get('USBINTERFACE')
    usbModem = '1e0e:9001' if gsmConf.get('USBMODEM') is None else gsmConf.get('USBMODEM')
    command = f'sudo sakis3g "connect"  DNS="{dns}" APN="CUSTOM_APN" CUSTOM_APN="{apn}" APN_USER="{apnUser}" APN_PASS="{apnPass}" USBINTERFACE="{usbInterface}" OTHER="USBMODEM" USBMODEM="{usbModem}"'
    try:
        if status == 1:
            subprocess.call([command], shell=True)
    except Exception as e:
        LOG.error('Error resetting modem : %s', e)
    time.sleep(5)
    LOG.info('GSM Status: %s', GPIO.input(statusPin))


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


readConfiguration()
setupPins()
while True:
    if internetPresent():
        continue
    resetModem()
    time.sleep(300)
