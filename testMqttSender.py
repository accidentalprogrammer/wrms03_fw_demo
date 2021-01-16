#!/usr/bin/env python

from MqttSender import MqttSender

sender = MqttSender()

print(sender.sendPayload( "This is a test payload " ))
