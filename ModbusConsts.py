#!/usr/bin/env python

##
#  @package ModbusConsts Package conataining all the constant values used in Modbus Modules
#

class ModbusConsts:

    QUERY_PARAMS = 'query_params'

    DEVICE_ID = 'device_id'
    DEVICE_TYPE = 'device_type'
    CONN_TYPE = 'connection_type'
    CONN_PARAMS = 'connection_param'

    DEVICE_CATEGORY = 'device_category'
    CAT_INVERTER = 'inverter'
    CAT_INVERTER_ABB33 = 'inverter_abb33'
    CAT_INVERTER_ABB100 = 'inverter_abb100'
    CAT_WST = 'wst'

    SLAVE_ID = 'slave_id'

    # Serial Connection parameters
    BAUDRATE = 'baud_rate'
    PARITY = 'parity'
    STOP_BITS = 'stop_bits'
    BYTE_SIZE = 'byte_size'

    # TCP Connection Paramters
    HOST = 'host'
    PORT = 'port'

    # Register parameters
    FUNCTION_ID = 'function_id'
    START_REG = 'start_register'
    REG_COUNT = 'register_count'

    # Connection types
    CONN_RTU = 'RTU'
    CONN_TCP = 'TCP'
    CONN_RTU_TCP = 'RTUoverTCP'
    CONN_RTU_LORA = 'RTUoverLORA'
    CONN_TYPE_SLAVE_RS485 = 'SlaveRS485'
    CONN_TYPE_SLAVE_LORA = 'SlaveLora'


    # TCS related constants
    TCS_DATA = 'tcs_data'
    TCS_LINK_TYPE = 'tcs_link_type'
    TCS_LINK_LORA_NODE = 'LoraNode'
    TCS_LINK_GATEWAY = 'gateway'
    TCS_SERVICE = 'tcs_service'
    TCS_VERSION = 'tcs_version'
    TCS_OFFERING = 'tcs_offering'
    TCS_OBS_SENSOR = 'obs_sensor'
    TCS_OBS_FEATURE = 'obs_feature'
    TCS_GEO_TYPE = 'tcs_geo_type'
    TCS_COORD_ALTITUDE = 'tcs_coord_alt'
    TCS_COORD_LATITUDE = 'tcs_coord_lat'
    TCS_COORD_LONGITUDE = 'tcs_coord_long'


    # Parity types
    PARITY_NONE = 'none'
    PARITY_EVEN = 'even'
    PARITY_ODD  = 'odd'
    PARITY_MARK = 'mark'
    PARITY_SPACE = 'space'

    # Stop bits
    SB_ONE = 1
    SB_ONE_POINT_FIVE = 1.5
    SB_TWO = 2

    # Byte sizes
    BYTE_FIVE = 5
    BYTE_SIX  = 6
    BYTE_SEVEN = 7
    BYTE_EIGHT = 8

    # Slave card params
    SLAVE_CARD_ID = 'slave_card_id'

    DEVICE_TYPE_DELTA = 'INVERTER_DELTA_RPIM3_SLAVE'
    DEVICE_TYPE_ABB33 = 'INVERTER_ABB_33KW_SLAVE'
    DEVICE_TYPE_ABB100 = 'INVERTER_ABB_100KW_SLAVE'
    DEVICE_TYPE_SLAVE_SENSOR = ''


    # Decoding config sections

    PREPROCESS = 'preprocess'
    VALUE_MAP = 'value_map'
    DATA = 'data'
    ALARM = 'alarm'
    DEFAULT = 'default'

    PARAMS = 'params'

    # Decoding parameter list
    PARAM_NAME = 'name'
    REG_SIZE = 'register_size'
    PARAM_SIZE = 'param_size'
    PARAM_TYPE = 'type'
    BYTE_OFFSET = 'byte_offset'
    BIT_OFFSET = 'bit_offset'
    SIGN = 'sign'
    FORMULA = 'formula'
    MAP_KEY = 'map_key'

    DEFAULT_VALUE = 'value'

    # Parameter types

    TYPE_INT = 'Integer'
    TYPE_FLOAT = 'Float'
    TYPE_STRING = 'String'
    TYPE_HEX = 'hex'
    TYPE_RAW = 'Raw'
    TYPE_SWAP_FLOAT_8 = 'SwappedFloat8'
    TYPE_SWAP_FLOAT_8R = 'SwappedFloat8R'
    TYPE_SWAP_FLOAT_16 = 'SwappedFloat16'
    TYPE_SWAP_INT_8 = 'SwappedInt8'
    TYPE_SWAP_INT_16 = 'SwappedInt16'

    SIGN_S = 'S'
    SIGN_U = 'U'

    PARAM_MIN = 'min_val'
    PARAM_MAX = 'max_val'


    # Solar Inverter Parameters
    SLR_WSNSR = 'WSNSR'
    SLR_TEMP = 'TEMP'
    SLR_HUMI = 'HUMI'
    SLR_RELAY = 'RELAY'
    SLR_RAIN = 'RAIN'
    SLR_WINDS = 'WINDS'
    SLR_WINDD = 'WINDD'
    SLR_ANLG1 = 'ANLG1'
    SLR_IPPWR = 'IPPWR'
    SLR_DCIP = 'DCIP'
    SLR_DCV = 'DCV'
    SLR_DCA = 'DCA'
    SLR_DCW = 'DVW'
    SLR_MDCIP = 'MDCIP'
    SLR_OPPWR = 'OPPWR'
    SLR_ACOP = 'ACOP'
    SLR_ACV = 'ACV'
    SLR_ACA = 'ACA'
    SLR_ACW = 'ACW'
    SLR_FRQ = 'FRQ'
    SLR_MACOP = 'MACOP'
    SLR_APP = 'APP'
    SLR_APP1 = 'APP1'
    SLR_APP2 = 'APP2'
    SLR_APP3 = 'APP3'
    SLR_EVT = 'EVT'
    SLR_RCP = 'RCP'
    SLR_COSFI = 'COSFi'
    SLR_PF = 'PF'
    SLR_STR = 'STR'
    SLR_WATTHT = 'WattH_T'
    SLR_RUNTT = 'RunT_T'
    SLR_WATTH = 'WattH'
    SLR_RUNT = 'RunT'
    SLR_OP_STATE = 'Op_State'
    SLR_REC_TIME = 'RecTime'

    #Weather Station Parameters
    WST_WSNSR = 'WSNSR'
    WST_TEMP = 'TEMP'
    WST_HUMI = 'HUMI'
    WST_RELAY = 'RELAY'
    WST_RAIN = 'RAIN'
    WST_WINDS = 'WINDS'
    WST_WINDD = 'WINDD'
    WST_ANLG1 = 'ANLG1'

    CUSTOM_ALARM_PROCESSORS = {}
