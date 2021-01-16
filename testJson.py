#!/usr/bin/env python

import simplejson as json
from MainConfig import MainConfig

print( MainConfig().CONFIG_PATH)

strjson = '{"key":"value"}'

jsonDict = None

try:
    jsonDict = json.loads( strjson )
except Exception as e:
    print(e)
print( jsonDict )

config = None
with open( '/home/himanshu/DataLogger/app/config/config.json', 'r' ) as f:
    config = json.load(f)

with open( '/home/himanshu/DataLogger/app/config/config.json', 'w' ) as f:
    config['mqtt_topic'] = 'new/topic'
    f.truncate()
    json.dump( config, f, indent=4 )
