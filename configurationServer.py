#!/usr/bin/env python

from flask import Flask, escape, request, send_from_directory
from flask_cors import CORS
import subprocess
import simplejson as json
from os import listdir, path

DEVICE_CONFIG_PATH = ''
MAIN_CONFIG_PATH = ''


app = Flask(__name__, static_folder='/root/DataLogger/app/config_backend/static')
CORS(app)

app.run(host = '0.0.0.0')


@app.route("/")
def rebootDevice():
    try:
        subprocess.call( 'reboot', shell=True )
    except Exception as e:
        print( 'Error syncing filesystem changes: %s', e )


@app.route("/")
def updateMainConfig( args ):
    
    try:
        params = args.get('params')
        if params is not None:
            mc = {}
            with open( MAIN_CONFIG_PATH ) as f:
                mc = json.load(f)
            for key,value in params.items():
                mc[key] = value

            with open( MAIN_CONFIG_PATH, 'w' ) as f:
                f.truncate()
                json.dump( mc, f, indent=4 )

            try:
                subprocess.call( 'sync', shell=True )
            except Exception as e:
                print( 'Error syncing filesystem changes: %s', e )

    except Exception as e:
        print('Error updating main config: %s', e)


@app.route("/")
def updateDeviceConfig( args ):
    try:
        newDeviceConfig = args.get('new_device_config')
        if newDeviceConfig is not None:
            with open( DEVICE_CONFIG_PATH, 'w' ) as f:
                f.truncate()
                json.dump( newDeviceConfig, f, indent=4 )
            try:
                subprocess.call( 'sync', shell=True )
            except Exception as e:
                print( 'Error syncing filesystem changes: %s', e )

    except Exception as e:
        print('Error replacing the device config with new config: %s', e)


@app.route("/")
def updateFirmware():
    pass