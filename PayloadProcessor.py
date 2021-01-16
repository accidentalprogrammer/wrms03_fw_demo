#!/usr/bin/env python

##
#  @package PayloadProcessor Package contains the functions to preprocess the payload in the
#  edge device before sending to the server

import logging
import xml.etree.ElementTree as ET
import ParamValueStore
import datetime
import time
import MainConfig
from Constants import Constants
from ModbusConsts import ModbusConsts

##
#
class SolarInverterProcessor:

    LOG = logging.getLogger( __name__ )

    ##
    #  Function to calculate the energy generated from morning and till the current time and populate in the payload
    #
    def populateTodayEnergy( self, payload ):
        root = ET.fromstring( payload )
        curDate = str(datetime.datetime.fromtimestamp(time.time()).strftime('%d'))
        todayEnergyDict = {}
        mc = MainConfig.MainConfig().getConfig()
        toCalcList = mc.get( Constants.TODAY_ENERGY_CALC_LIST )
        for DT in root:
            for controller in DT:
                tenergyElm = None
                if controller.tag == 'SINV':
                    invId = controller.attrib['id']
                    invType = controller.attrib['type']
                    if invType not in toCalcList:
                        continue

                    ps = ParamValueStore.ParamValueStore().getValueStore()
                    print(invId)
                    for elems in controller:
                        if elems.tag == 'WattH':
                            totalEnergy = elems.attrib.get( 'V' )
                            if ps.get( invId ) is not None:
                                invStore = ps.get( invId )
                                prevEnergy = 0 if invStore.get( 'prev_energy' ) is None else invStore.get( 'prev_energy' )
                                totalEnergy = prevEnergy if float(totalEnergy) < float(prevEnergy) else totalEnergy
                                if invStore.get( 'WattH_T' ) is not None:
                                    todayEnergy = invStore.get( 'WattH_T' )
                                    keys = []
                                    print(todayEnergy)
                                    for key,val in todayEnergy.items():
                                        if int(key) < int(curDate):
                                            keys.append(key)

                                    for key in keys:
                                        todayEnergy.pop(key, None)
                                    print(todayEnergy)
                                    if todayEnergy.get(curDate) is None:
                                        todayEnergy[curDate] = 0

                                    try:
                                        todayEnergy[curDate] = float(todayEnergy[curDate]) + (float(totalEnergy) - float(prevEnergy))
                                    except Exception as e:
                                        print(e)
                                    print('Prev: ', prevEnergy)
                                    print('Cur: ', totalEnergy)
                                    print(todayEnergy)
                                    ps[invId]['WattH_T'] = todayEnergy
                                    tenergyElm = ET.Element('WattH_T', attrib={'V': str(todayEnergy[curDate])})
                                else:
                                    tenergyElm = ET.Element('WattH_T', attrib={'V': str(todayEnergy[curDate])})
                                    ps[invId]['WattH_T'] = { curDate:0 }
                                invStore['prev_energy'] = totalEnergy
                            else:
                                tenergyElm = ET.Element( 'WattH_T', attrib={'V':'0'} )
                                ps[invId] = { 'WattH_T': { curDate:0 } }

                    controller.append(tenergyElm)
                    ParamValueStore.ParamValueStore().storeValues(ps)

        return ET.tostring(root)


    def populateTodayEnergyJson( self, payload ):
        gtwyId = list(payload.keys())[0]
        curDate = str(datetime.datetime.fromtimestamp(time.time()).strftime('%d'))
        todayEnergyDict = {}
        mc = MainConfig.MainConfig().getConfig()
        toCalcList = mc.get( Constants.TODAY_ENERGY_CALC_LIST )
        payloadArr = payload.get(gtwyId)
        for pyld in payloadArr:
            invArr = pyld.get( 'inverters' )
            print(invArr)
            if invArr is None:
                continue

            for inv in invArr:
                todayEnergyVal = 0
                invId = inv.get('device_id')
                devType = inv.get('device_type')
                if devType not in toCalcList:
                    continue
                ps = ParamValueStore.ParamValueStore().getValueStore()
                totalEnergy = inv.get('total_energy', '0.0')
                if ps.get( invId ) is not None:
                    invStore = ps.get( invId )
                    prevEnergy = 0 if invStore.get( 'prev_energy' ) is None else invStore.get( 'prev_energy' )
                    totalEnergy = prevEnergy if float(totalEnergy) < float(prevEnergy) else totalEnergy
                    if invStore.get( 'today_energy' ) is not None:
                        todayEnergy = invStore.get( 'today_energy' )
                        keys = []
                        print(todayEnergy)
                        for key,val in todayEnergy.items():
                            if int(key) < int(curDate):
                                keys.append(key)

                        for key in keys:
                            todayEnergy.pop(key, None)
                        print(todayEnergy)
                        if todayEnergy.get(curDate) is None:
                            todayEnergy[curDate] = 0

                        try:
                            todayEnergy[curDate] = float(todayEnergy[curDate]) + (float(totalEnergy) - float(prevEnergy))
                        except Exception as e:
                            print(e)
                        ps[invId]['today_energy'] = todayEnergy
                        todayEnergyVal = todayEnergy[curDate]
                    else:
                        todayEnergyVal = todayEnergy[curDate]
                        ps[invId]['today_energy'] = { curDate:0 }

                    invStore['prev_energy'] = totalEnergy
                else:
                    todayEnergyVal = 0
                    ps[invId] = { 'today_energy': { curDate:0 } }

                inv['today_energy'] = todayEnergyVal
                ParamValueStore.ParamValueStore().storeValues(ps)

        return payload

##
#
class WSTSensorProcessor:

    LOG = logging.getLogger( __name__ )


    def mergeWStXml( self, payload ):
        wstElm = ET.Element('WST', attrib={'id': 'WST001', 'type':'WST_STM8_RS485'})

        root = ET.fromstring( payload )
        for DT in root:
            if DT.tag == 'DT':
                for controller in DT:
                    if controller.tag == 'WST':
                        wstId = controller.attrib['id']
                        wstType = controller.attrib['type']
                        print(wstId)
                        for elems in controller:
                            wstElm.append(elems)

        if wstElm.find('WSNSR') is None:
                wsnsr = ET.Element('WSNSR', attrib={'V': '0'})
                wstElm.append(wsnsr)
        if wstElm.find('TEMP') is None:
                temp = ET.Element('TEMP', attrib={'V': '0'})
                wstElm.append(temp)
        if wstElm.find('HUMI') is None:
                humi = ET.Element('HUMI', attrib={'V': '0'})
                wstElm.append(humi)
        if wstElm.find('RELAY') is None:
                relay = ET.Element('RELAY', attrib={'V': '0'})
                wstElm.append(relay)
        if wstElm.find('RAIN') is None:
                rain = ET.Element('RAIN', attrib={'V': '0'})
                wstElm.append(rain)
        if wstElm.find('WINDS') is None:
                winds = ET.Element('WINDS', attrib={'V': '0'})
                wstElm.append(winds)
        if wstElm.find('WINDD') is None:
                windd = ET.Element('WINDD', attrib={'V': '0'})
                wstElm.append(windd)


        for DT in root:
            if DT.tag == 'DT':
                while DT.find('WST') is not None:
                    el = DT.find('WST')
                    DT.remove(el)
                DT.append(wstElm)

        return ET.tostring(root)

    
    def mergeWstJson( self, payload ):
        ignoreList = [ 'device_id', 'device_type', 'device_category', 'slave_id' ]
        gtwyId = list(payload.keys())[0]  # Change how we get gateway id, we should get it from the configuration file

        payloadArr = payload.get(gtwyId)
        for pyld in payloadArr:
            wstArr = pyld.get( ModbusConsts.CAT_WST )
            print(wstArr)
            if wstArr is None:
                continue

            combinedWst = {}
            combinedWst['device_id'] = 'WST001'
            combinedWst['device_type'] = 'WST_STM8_RS485'
            combinedWst['device_category'] = 'WST'

            for wst in wstArr:
                for key,value in wst.items():
                    if key not in ignoreList:
                        combinedWst[key] = value
            
            newWstArr = []
            newWstArr.append(combinedWst)
            pyld[ModbusConsts.CAT_WST] = newWstArr

        return payload
