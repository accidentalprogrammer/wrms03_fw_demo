#!/usr/bin/env python


##
#  @package MqttSender Module contains the functionality to send the message over MQTT protocol
#


import paho.mqtt.client as mqtt
import logging
from MainConfig import MainConfig
from Constants  import Constants
import GsmUtility
import time

client = None
connected = False


##
#
def on_connect( mclient, userdata, flags, rc):
    global connected
    print( " Connect with result code ",rc )
    if rc == 0:
        connected = True

##
#
def on_disconnect( mclient, userdata, rc):
    global client
    global connected
    print( "Client got disconnected", rc )
    client = None
    connected = False

##
#
def on_publish( mclient, userdata, mid ):
    print("Message published")
    print(mid)


class MqttSender:

    LOG = logging.getLogger( __name__ )

    MQTT_HOST = None
    MQTT_PORT = None
    MQTT_TLS = None
    MQTT_QOS = None
    MQTT_TOPIC = None

    ##
    #
    def initConnection( self ):
        global client
        global on_connect
        global on_disconnect
        global on_publish

        mc = MainConfig().getConfig()
        self.MQTT_HOST = mc.get( Constants.MQTT_HOST )
        self.MQTT_PORT = mc.get( Constants.MQTT_PORT )
        self.MQTT_TLS = True if mc.get( Constants.MQTT_TLS ) is None or mc.get( Constants.MQTT_TLS ) == 'Y' else False
        self.MQTT_QOS = mc.get( Constants.MQTT_QOS )
        self.MQTT_TOPIC = mc.get( Constants.MQTT_TOPIC )
        if client is None:

            if self.MQTT_TLS:
                pass
            else:
                client = mqtt.Client( client_id=Status.deviceId )
                client.on_connect = on_connect
                client.on_disconnect = on_disconnect
                client.on_publish = on_publish

                try:
                    client.connect( self.MQTT_HOST, port=self.MQTT_PORT, keepalive=600 )
                    client.loop_start()
                except Exception as e:
                    self.LOG.error( "Error conncting to MQTT server: %s", e )


    ##
    #
    def sendPayload( self, payload ):
        global client
        self.initConnection()

        result = False

        if client is None :
            return result

        resp = client.publish( topic=self.MQTT_TOPIC, payload=payload, qos=self.MQTT_QOS, retain=False)
        print(resp)
        return True
