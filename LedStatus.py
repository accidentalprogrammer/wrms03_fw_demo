#!/usr/bin/env python

##
#  @package LedStatus Module contains the functions to control the status of the LEDs
#

import threading
import logging
import OPi.GPIO as GPIO
import time

LED_OFF = 0
LED_STABLE = 1
LED_BLINK = 2

stop = False
led_status = LED_OFF

class LedStatus ( threading.Thread ):

    LOG = logging.getLogger( __name__ )

    def __init__( self ):
        threading.Thread.__init__( self )

    def run( self ):
        self.LOG.debug( 'LedStatus Thread started' )

        GPIO.setup(26, GPIO.OUT)

        global stop
        global led_status
        global LED_OFF
        global LED_STABLE
        global LED_BLINK

        while (True):
            if stop:
                break

            if led_status == LED_OFF:
                self.led_off()
            elif led_status == LED_STABLE:
                self.led_stable()
            elif led_status == LED_BLINK:
                self.toggle_led( 0.5 )
            else:
                self.led_off()
            time.sleep( 1 )


    def toggle_led( self, time_period ):
        GPIO.output(26, GPIO.HIGH)
        time.sleep(time_period)
        GPIO.output(26, GPIO.LOW)
        time.sleep(time_period)


    def led_stable( self ):
        GPIO.output(26, GPIO.LOW)

    def led_off( self ):
        GPIO.output(26, GPIO.HIGH)
