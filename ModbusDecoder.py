#!/usr/bin/env python


##
#  @package ModbusDecoder Module contains logic for decoding the Modbus register data
#

import logging
from ModbusConsts import ModbusConsts
from ModbusDeviceConfig import ModbusDeviceConfig
import ModbusUtils
from SimpleEval import SimpleEval
import re
import struct


class ModbusDecoder:

    LOG = logging.getLogger( __name__ )

    ##
    #  Function to decode the modbus register queried from the Modbus Devices and return a list of dictionaries containing data in key/value format
    #  @param modbusResponseList List: List containing the datasets of all the Modbus devices
    #
    #  @return decodedList List: List containing the decoded Modbus data for all the devices
    #
    def decodeModbusData( self, modbusResponseList ):

        decodedList = []
        for modbusResponse in modbusResponseList:
            self.LOG.debug( 'Modbus response: %s', modbusResponse )
            decodedResponse = {}
            deviceType = modbusResponse.get( ModbusConsts.DEVICE_TYPE )
            slaveId = modbusResponse.get( ModbusConsts.SLAVE_ID )
            devCategory = modbusResponse.get( ModbusConsts.DEVICE_CATEGORY )
            devId = modbusResponse.get( ModbusConsts.DEVICE_ID )

            try:
                modbusConfig = ModbusDeviceConfig().getModbusConfig( deviceType )
            except Exception as e:
                self.LOG.error('Error getting the decoding file: %s', e)

            if modbusConfig is None:
                self.LOG.warn( 'Device not supported: %s', deviceType )
                continue

            decodedResponse[ModbusConsts.DEVICE_TYPE] = deviceType
            decodedResponse[ModbusConsts.SLAVE_ID] = slaveId
            decodedResponse[ModbusConsts.DEVICE_CATEGORY] = devCategory
            decodedResponse[ModbusConsts.DEVICE_ID] = devId

            data = {}
            alarms = {}

            try:
                if ModbusConsts.PREPROCESS in modbusConfig:
                    self.processSection( data, modbusResponse, modbusConfig.get( ModbusConsts.PREPROCESS ), modbusConfig.get( ModbusConsts.VALUE_MAP ) )

                if ModbusConsts.DATA in modbusConfig:
                    self.processSection( data, modbusResponse, modbusConfig.get( ModbusConsts.DATA ), modbusConfig.get( ModbusConsts.VALUE_MAP ) )

                if ModbusConsts.ALARM in modbusConfig:
                    self.processSection( alarms, modbusResponse, modbusConfig.get( ModbusConsts.ALARM ), modbusConfig.get( ModbusConsts.VALUE_MAP ) )

                if ModbusConsts.DEFAULT in modbusConfig:
                    self.processDefault( data, modbusConfig.get( ModbusConsts.DEFAULT ) )
            except Exception as e:
                pass

            decodedResponse[ModbusConsts.DATA] = data
            decodedResponse[ModbusConsts.ALARM] = alarms

            decodedList.append( decodedResponse )

        return decodedList



    ##
    #  Function to fill in the default values for the parameters in case any register set does not contain the data
    #
    #  @param decodedResponse dictionary: Dictionary conataining the decoded parameters
    #  @param param dictionary: dictionary containing the decoding details for a parameter
    #
    def fillDefault( self, decodedResponse, param ):

        name = param.get( ModbusConsts.PARAM_NAME )
        type = param.get( ModbusConsts.PARAM_TYPE )

        if type == ModbusConsts.TYPE_INT or type == ModbusConsts.TYPE_SWAP_INT_8 or type == ModbusConsts.TYPE_SWAP_INT_16:
            decodedResponse[name] = 0
        elif type == ModbusConsts.TYPE_FLOAT or type == ModbusConsts.TYPE_SWAP_FLOAT_8 or type == ModbusConsts.TYPE_SWAP_FLOAT_16:
            decodedResponse[name] = 0.0
        elif type == ModbusConsts.TYPE_STRING:
            decodedResponse[name] = 'NA'


    ##
    #  Function replaces all the words starting with '$' in the string expression with their corresponding value in the decoded data
    #  If the decoded value is not found in the dictionary, the expression is reduced to 0 and the function returns
    #
    #  @param decodedResponse dictionary: dictionary conataining the previously decoded data
    #  @param expr string: string in which values need to be replaced
    #
    #  @return expr string: string with all the parameter values replaced
    #
    def replaceValue( self, decodedResponse, expr ):
        matched = re.findall( r'\$\w*', expr, flags=0 )
        for match in matched:
            key = match.replace( '$', '' )
            findVal = decodedResponse.get( key )
            if key is None:
                expr = '0'
                return expr
            expr = expr.replace( match, str( findVal ) )

        return expr


    ##
    #  Function to get integer value from the bytes.
    #
    #  @param decodedResponse dictionary: dictionary containing all the decoded data
    #  @param data bytearray: bytearray containing the raw data
    #  @param param dictionary: dictionary containing the decoding information for the parameter
    #
    #  @return intVal int: Decoded integer value
    #
    def getIntegerValue( self, decodedResponse, data, param ):
        valSize = param.get( ModbusConsts.PARAM_SIZE )
        sign = ModbusConsts.SIGN_U
        if ModbusConsts.SIGN in param:
            sign = param.get( ModbusConsts.SIGN )

        signBitMask = 0x01 << (valSize-1)
        intVal = ModbusUtils.bytesToInt( data )
        self.LOG.debug( 'Data: %s',data )
        signBit = intVal & signBitMask
        signBit = signBit >> (valSize -1)
        if signBit == 1 and sign == ModbusConsts.SIGN_S:
            if valSize == 8:
                intVal = -0x100 + intVal
            elif valSize == 16:
                intVal = -0x10000 + intVal
            elif valSize == 32:
                intVal = -0x100000000 + intVal

        if ModbusConsts.FORMULA in param:
            formula = param.get( ModbusConsts.FORMULA )
            formula = formula.replace( '$this', str( intVal ) )
            formula = self.replaceValue( decodedResponse, formula )
            s = SimpleEval()
            intVal = s.eval( formula )

        if ModbusConsts.PARAM_MAX in param:
            maxVal = param.get( ModbusConsts.PARAM_MAX )
            if intVal > maxVal:
                intVal = maxVal

        if ModbusConsts.PARAM_MIN in param:
            minVal = param.get( ModbusConsts.PARAM_MIN )
            if intVal < minVal:
                intVal = minVal

        return intVal


    ##
    #  Function to decode the bytes into IEEE 754 float value
    #
    #  @param decodedResponse dictionary: dictionary containing all the decoded data
    #  @param data bytearray: bytearray containing the raw data
    #  @param param dictionary: dictionary containing the decoding information for the parameter
    #
    #  @return intVal int: Decoded Float value
    #
    def getFloatValue( self, decodedResponse, data, param ):
        [floatVal] = struct.unpack( 'f', data )

        if ModbusConsts.FORMULA in param:
            formula = param.get( ModbusConsts.FORMULA )
            formula = formula.replace( '$this', str( floatVal ) )
            formula = self.replaceValue( decodedResponse, formula )
            s = SimpleEval()
            floatVal = s.eval( formula )

        if ModbusConsts.PARAM_MAX in param:
            maxVal = param.get( ModbusConsts.PARAM_MAX )
            if floatVal > maxVal:
                floatVal = maxVal


        if ModbusConsts.PARAM_MIN in param:
            minVal = param.get( ModbusConsts.PARAM_MIN )
            if floatVal < minVal:
                floatVal = minVal

        return floatVal



    ##
    #  Function to map the decoded value to a predefined set of values. Returns the mapped value if found
    #  or the original value if no mapping exists
    #
    #  @param value variable: decoded value of the parameter
    #  @param mapKey string: key of the map containing the mappings for this value
    #  @param valueMap list: List containing the maps
    #
    def getMappedValue( self, value, mapKey, valueMap ):
        if valueMap is None:
            return value

        vmap = valueMap.get( mapKey )
        if vmap is None:
            return 'Unknown'

        mappedVal = None
        try:
            mappedVal = vmap.get( str( value ) )
        except Exception as e:
            self.LOG.error('Error mapping the value: %s', e)

        if mappedVal is None:
            return 'Unknown'
        else:
            return mappedVal


    ##
    #  Function to decode the parameter based on the type and store the decoded value in the supplied dictionary
    #
    #  @param decodedResponse dictionary: dictionary to store the decoded data
    #  @param data bytearray: bytearray containing the raw data
    #  @param param dictionary: dictionary containing the decoding information for the parameter
    #
    def decodeParam( self, decodedResponse, data, param, valueMap ):
        name = param.get( ModbusConsts.PARAM_NAME )
        type = param.get( ModbusConsts.PARAM_TYPE )

        if type == ModbusConsts.TYPE_INT:
            intVal = self.getIntegerValue( decodedResponse, data, param )
            value = "%.2f"%intVal if isinstance(intVal, float) else intVal
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_SWAP_INT_8:
            data = data[::-1]
            intVal = self.getIntegerValue( decodedResponse, data, param )
            value = "%.2f"%intVal if isinstance(intVal, float) else intVal
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_SWAP_INT_16:
            data = ModbusUtils.reverseTwoElements( data )
            print('Swapped Data: ', data)
            intVal = self.getIntegerValue( decodedResponse, data, param )
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            value = "%.2f"%intVal if isinstance(intVal, float) else intVal
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_FLOAT:
            data = data[::-1] # Reverse the data for correct endianness
            floatVal = self.getFloatValue( decodedResponse, data, param )
            value = "%.2f"%floatVal
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_SWAP_FLOAT_8:
            floatVal = self.getFloatValue( decodedResponse, data, param )
            value = "%.2f"%floatVal
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_SWAP_FLOAT_8R:
            data = data[::-1]
            newData = [ data[1], data[0], data[3], data[2] ]
            floatVal = self.getFloatValue( decodedResponse, bytearray(newdata), param )
            value = "%.2f"%floatVal
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_SWAP_FLOAT_16:
            data = data[::-1] # Reverse the data for correct endianness
            data = ModbusUtils.reverseTwoElements( data )
            floatVal = self.getFloatValue( decodedResponse, bytearray(data), param )
            value = "%.2f"%floatVal
            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        elif type == ModbusConsts.TYPE_STRING:
            stringVal = data.decode('ascii')
            decodedResponse[name] = stringVal

    ##
    #
    def processParam( self, decodedResponse, regData, param, valueMap ):
        regSize = param.get( ModbusConsts.REG_SIZE )
        paramSize = param.get( ModbusConsts.PARAM_SIZE )
        byteOffset = param.get( ModbusConsts.BYTE_OFFSET )
        if paramSize >= regSize or regSize < 8:
            if byteOffset >= len( regData ):
                self.fillDefault( decodedResponse, param )  # Byte offset of the parameter lies outside the length of register set data
                return
            endIdx = int( byteOffset + ( paramSize/8 ) )
            data = regData[byteOffset: endIdx]
            self.decodeParam( decodedResponse, data, param, valueMap )
        else:
            bitOffset = param.get( ModbusConsts.BIT_OFFSET )
            if bitOffset >= regSize:
                self.fillDefault( decodedResponse, param )
                return
            endIdx = int( byteOffset + ( regSize/8 ) )
            data = regData[byteOffset:endIdx]
            self.decodeBitwiseValue( decodedResponse, data, param, valueMap )


    ##
    #
    def processSection( self, decodedResponse, modbusResponse, regsetList, valueMap ):
        for regSet in regsetList:
            funId = "%02X"%regSet.get( ModbusConsts.FUNCTION_ID )
            sor = "%04X"%regSet.get( ModbusConsts.START_REG )
            regsetKey = funId + "_" + sor
            regData = modbusResponse.get( regsetKey )
            if regData is None:
                self.LOG.warning( 'Register data is empty for %s. Default values will be filled.', regsetKey )
                for param in regSet.get( ModbusConsts.PARAMS ):
                    self.fillDefault( decodedResponse, param )
                continue

            for param in regSet.get ( ModbusConsts.PARAMS ):
                self.LOG.debug('Decoding param: %s', param )
                self.processParam( decodedResponse, regData, param, valueMap )



    ##
    #  Function to fill in the default values for the parameters which are not provided by the specific controller
    #  @param decodedResponse dictionary: dictionary containing all the decoded parameters
    #  @param defaultList List: List containing the default parameters
    #
    def processDefault( self, decodedResponse, defaultList ):
        for param in defaultList:
            name = param.get( ModbusConsts.PARAM_NAME )
            value = param.get( ModbusConsts.DEFAULT_VALUE )
            decodedResponse[name] = value


    ##
    #  Function to get the bitwise value from the given register data
    #
    #  @param decodedResponse dictionary: dictionary containing all the decoded parameters
    #  @param data bytearray: bytearray containing the register data
    #  @param param dictionary: dictionary containing the decoding information for the parameters
    #
    def decodeBitwiseValue( self, decodedResponse, data, param, valueMap ):
        name = param.get( ModbusConsts.PARAM_NAME )
        type = param.get( ModbusConsts.PARAM_TYPE )

        if type == ModbusConsts.TYPE_INT:
            intRegVal = ModbusUtils.bytesToInt( data )
            bitOffset = param.get( ModbusConsts.BIT_OFFSET )
            size = param.get( ModbusConsts.PARAM_SIZE )
            mask = 0x00
            mask = ~mask
            mask = mask << size
            mask = ~mask
            mask = mask << bitOffset
            value = mask & intRegVal
            value = value >> bitOffset
            if ModbusConsts.FORMULA in param:
                formula = param.get( ModbusConsts.FORMULA )
                formula = formula.replace( '$this', str( value ) )
                formula = self.replaceValue( decodedResponse, formula )
                s = SimpleEval()
                value = s.eval( formula )

            if ModbusConsts.PARAM_MAX in param:
                maxVal = param.get( ModbusConsts.PARAM_MAX )
                if value > maxVal:
                    value = maxVal

            if ModbusConsts.PARAM_MIN in param:
                minVal = param.get( ModbusConsts.PARAM_MIN )
                if value < minVal:
                    value = minVal

            if ModbusConsts.MAP_KEY in param:
                value = self.getMappedValue( value, param.get(ModbusConsts.MAP_KEY), valueMap )
            decodedResponse[name] = value
        else:
            pass

