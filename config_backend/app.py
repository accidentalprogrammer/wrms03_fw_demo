from flask import Flask, escape, request, send_from_directory
from flask_cors import CORS
import simplejson as json
from os import listdir, path


app = Flask(__name__, static_folder='/root/DataLogger/app/config_backend/static')
CORS(app)

app.run(host = '0.0.0.0')

@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/addModbusDevice.html")
def addModbusDevice():
    return app.send_static_file('addModbusDevice.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('/root/DataLogger/app/config_backend/static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('/root/DataLogger/app/config_backend/static/css', path)

@app.route("/getMainConfig")
def getMainConfig():
    mconfig = {}
    try:
        with open( '/root/DataLogger/config/config.json' ) as f:
            mconfig = json.load(f)
    except Exception as e:
        pass
    return json.dumps(mconfig)

@app.route("/getDeviceList")
def getDeviceList():
    devList = []
    try:
        with open( '/root/DataLogger/modbus_dev/devices.json' ) as f:
            devList = json.load(f)
    except Exception as e:
        pass
    return json.dumps(devList)

@app.route( "/updateMainConfig" , methods = ['GET', 'POST'])
def updateMainConfig():
    data = request.get_data()
    config = data.decode("utf-8")
    configJsonNew = json.loads(config)
    configJsonOld = None
    try:
        with open( '/root/DataLogger/config/config.json', 'r' ) as f:
            configJsonOld = json.load(f)
    except Exception as e:
        pass

    for key, value in configJsonNew.items():
        if value != 'Null':
            configJsonOld[key] = value

    try:
        with open( '/root/DataLogger/config/config.json', 'w' ) as f:
            f.truncate( 0 )
            json.dump( configJsonOld, f, indent=4 )
    except Exception as e:
        pass

    return '{"msg":"success"}'

@app.route( "/updateDeviceList", methods = ['GET', 'POST'] )
def updateDeviceList():
    data = request.get_data()
    devList = data.decode("utf-8")
    devListJson = json.loads(devList)
    try:
        with open( '/root/DataLogger/modbus_dev/devices.json', 'w' ) as f:
            f.truncate( 0 )
            json.dump( devListJson, f, indent=4 )
    except Exception as e:
        pass
    return '{"msg":"success"}'


@app.route( "/getDeviceTypes", methods = ['GET', 'POST'] )
def getDeviceTypes():
    fileList = [ f for f in listdir( '/root/DataLogger/app/modbus_config/' ) if path.isfile( '/root/DataLogger/app/modbus_config/'+f )]
    deviceTypes = []
    for configFile in fileList:
        truncPoint = configFile.find( '.' ) if configFile.find( '.' ) > -1 else len( configFile )
        configKey = configFile[:truncPoint].upper()
        deviceTypes.append(configKey)
    return json.dumps(deviceTypes)
