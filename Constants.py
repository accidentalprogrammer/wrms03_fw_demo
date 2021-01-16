#!/usr/bin/env python

##
# @package Constants Module contains the Constants definition for the
#

class Constants:

    GATEWAY_ID = 'gateway_id'

    SEVRER_CONN_TYPE = 'conn_type'
    SERVER_HTTP_URL = 'http_url'
    SERVER_IP = 'host'
    SERVER_PORT = 'port'

    PERIODIC_INTERVAL = 'periodic_interval'

    DATA_COMM_TYPE = 'data_comm_type'
    COMM_TYPE_HTTP = 'http'
    COMM_TYPE_MQTT = 'mqtt'
    COMM_TYPE_FTP = 'ftp'

    PAYLOAD_TYPE = 'payload_type'
    PAYLOAD_TYPE_JSON = 'json'
    PAYLOAD_TYPE_XML = 'xml'
    PAYLOAD_TYPE_TCS = 'tcs'

    MQTT_HOST = 'mqtt_host'
    MQTT_PORT = 'mqtt_port'
    MQTT_TLS = 'mqtt_tls'
    MQTT_QOS = 'mqtt_qos'
    MQTT_TOPIC = 'mqtt_topic'

    FTP_URL = 'ftp_url'
    FTP_USER = 'ftp_user'
    FTP_PWD = 'ftp_pwd'
    FTP_DIR = 'ftp_dir'

    UPDATE_TYPE = 'upg_type'
    UPG_TYPE_REPO = 'type_repo'
    UPG_TYPE_ARCHIVE = 'type_archive'
    UPG_TYPE_APT = 'type_apt'

    UPDATE_REPO = 'update_repo'
    UPDATE_REPO_USER = 'repo_user'
    UPDATE_REPO_PWD = 'repo_pwd'

    UPDATE_ARCHIVE_URL = 'archive_url'
    MAIN_CONFIG_UPDATE_URL = 'main_config_url'
    MODBUS_CONFIG_UPDATE_URL = 'modbus_config_url'

    CONFIG_REPO_FIX = 'config_repo_fix'
    CONFIG_REPO_SEC = 'config_repo'
    FW_REPO_FIX = 'fw_repo_fix'
    FW_REPO = 'fw_repo'
    CONFIG_REPO_URL = 'url'
    REPO_USER = 'user'
    REPO_PWD = 'password'

    MAIN_CONFIG_URL = 'main_config_url_server'
    MODBUS_CONFIG_URL = 'modbus_config_url_server'
    MAIN_CONFIG_URL_FIX = 'main_config_url_server_fix'
    MODBUS_CONFIG_URL_FIX = 'modbus_config_url_server_fix'
    FW_SERVER_URL = 'fw_server_url'
    FW_SERVER_URL_FIX = 'fw_server_url_fix'

    DEVICE_ID = 'device_id'
    LORA_CHANNEL = 'lora_channel'

    FW_UPG_INFO_FILE = '/root/UpdateAvailable'

    TODAY_ENERGY_CALC_LIST = 'today_energy_calc_list'
