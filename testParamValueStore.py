#!/usr/bin/env python

import ParamValueStore


ps = ParamValueStore.ParamValueStore().getValueStore()

print(ps)

ps['ABB00'] = { 'WattH_T': { '1575967974': 123456 } }

ParamValueStore.ParamValueStore().storeValues( ps )

ps = ParamValueStore.ParamValueStore().getValueStore()

print(ps)
