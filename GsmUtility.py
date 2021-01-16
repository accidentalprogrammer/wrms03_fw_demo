#!/usr/bin/env python


##
#  @package GsmUtility Module contains miscelaneous utility functions related to GSM modem

import serial
import time
import logging
import socket
import requests
import simplejson as json
import subprocess
import OPi.GPIO as GPIO


LOG = logging.getLogger( __name__ )



# Pin Definitons:
onPin = 16
pwrKey = 12
statusPin = 18


##
#
def resetModem():
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(onPin, GPIO.OUT)
        GPIO.setup(pwrKey, GPIO.OUT)
        GPIO.setup(statusPin, GPIO.IN)
    except Exception as e:
        pass

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
            subprocess.call(['sudo sakis3g "connect"  DNS="8.8.8.8" APN="CUSTOM_APN" CUSTOM_APN="airtelgprs.com" APN_USER="user" APN_PASS="pass" USBINTERFACE="3" OTHER="USBMODEM" USBMODEM="1e0e:9001"'], shell=True)
    except Exception as e:
        print(e)
    time.sleep(5)
    print('GSM Status: ', GPIO.input(statusPin))




##
#
def getGsmImeiNumber():

    data = None
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB2',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        ser.write('AT+CGSN\r\n'.encode())
        ser.flush()
        ser.flushOutput()
        time.sleep(1)
        size = ser.inWaiting()
        LOG.debug( 'Data in waiting: %s', size )
        if size > 0:
            data = ser.read(size)
            data = data.decode('utf-8')
            data = data[data.index('\n')+1:]
            data = data[:data.index('\n')]
            data = data.strip()
        LOG.debug( 'IMEI read: %s', data )
    except Exception as e:
        LOG.error( 'Error reading IMEI number: %s',e )
    finally:
        if ser is not None:
            ser.close()

    return data


ImeiNumber='0123456789'


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



def getServiceProvider():
    data = None
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB2',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        ser.write('AT+CSPN?\r\n'.encode())
        ser.flush()
        ser.flushOutput()
        time.sleep(1)
        size = ser.inWaiting()
        LOG.debug( 'Data in waiting: %s', size )

        if size > 0:
            data = ser.read(size)
            data = data.decode('utf-8')
            dataArr1 = data.split(':')
            dataArr2 = dataArr1[1].split(',')
            spName = dataArr2[0]
            spName = spName.replace('"', '')
            data = spName.strip()
    except Exception as e:
        print(e)
    try:
        ser.close()
    except:
        pass
    return data


def setSmsInTextMode():
    success = False
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB2',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        ser.write('AT+CMGF=1\r\n'.encode())
        ser.flush()
        ser.flushOutput()
        time.sleep(1)
        size = ser.inWaiting()
        LOG.debug( 'Data in waiting: %s', size )

        if size > 0:
            data = ser.read(size)
            data = data.decode('utf-8')
            if 'OK' in data:
                success = True
    except Exception as e:
        print(e)
    try:
        ser.close()
    except:
        pass
    return success


def getSmsIndexes():
    smsList = None
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB2',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        ser.write('AT+CMGD=?\r\n'.encode())
        ser.flush()
        ser.flushOutput()
        time.sleep(1)
        size = ser.inWaiting()
        LOG.debug( 'Data in waiting: %s', size )

        if size > 0:
            data = ser.read(size)
            data = data.decode('utf-8')
            if '+CMGD' not in data:
                return None
            startIdx = data.find("(")
            endIdx = data.find(")")
            if startIdx < 0 or endIdx < 0:
                return None
            csList = data[startIdx+1:endIdx]
            smsListStr = csList.split(',')
            smsList = []
            for sms in smsListStr:
                try:
                    smsList.append(int(sms))
                except:
                    pass
    except Exception as e:
        print(e)
    try:
        ser.close()
    except:
        pass
    return smsList


def readSmsAtIndex( idx ):
    data = None
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB2',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        cmd = f'AT+CMGR={idx}\r\n'
        ser.write(cmd.encode())
        ser.flush()
        ser.flushOutput()
        time.sleep(1)
        size = ser.inWaiting()
        LOG.debug( 'Data in waiting: %s', size )

        if size > 0:
            dataTemp = ser.read(size)
            data = data.decode('utf-8')
    except Exception as e:
        print(e)
    try:
        ser.close()
    except:
        pass
    return data


def getSmsContent( rawSms ):
    smsContent = None
    try:
        smsLines = rawSms.split('\r\n')
        idx = 0
        for line in smsLines:
            idx += 1
            if '+CMGR:' in line:
                break
        print('sms content: ')
        print(smsLines[idx])
    except Exception as e:
        print(e)

    return smsContent


def 