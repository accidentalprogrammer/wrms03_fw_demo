#!/bin/bash


deviceId=`grep device_id /root/DataLogger/config/config.json  | cut -d '"' -f 4 | xargs`
upgInfoFile="/root/UpdateAvailable"
logFile="/root/Update.log"
repoUpdateDir="/root/fwupg"
archiveUpdatePath="/root/GATEWAY.zip"
modbusConfigUpdatePath="/root/ModbusConfigUpdate"
mainConfigUpdatePath="/root/MainConfigUpdate"
fwPath="/root/DataLogger/app"
mainConfigPath="/root/DataLogger/config"
modbusConfigPath="/root/DataLogger/app/modbus_config"
mainConfigFile="/root/DataLogger/config/config.json"
modbusConfigFile="/root/DataLogger/modbus_dev/devices.json"



if [ -e "$upgInfoFile" ]
then
    updateType=`cat $upgInfoFile | xargs`
    if [ "$updateType" == "FW_UPDATE_REPO" ]
    then
        echo `date` ": Repo Update found" >> $logFile
        if [ -d "$repoUpdateDir" ]; then
            echo `date` ": Repo update directory exists" >> $logFile
            currentVer=`cat $fwPath/version.info | xargs`
            newVer=`cat $repoUpdateDir/version.info | xargs`
            if [ "$newVer" -gt "$currentVer" ]; then
                echo `date` ": New version is higher than current version, Update wiil be applied" >> $logFile
                rm -rf $fwPath
                mkdir $fwPath
                cp -r $repoUpdateDir/* $fwPath/
            fi
            rm $upgInfoFile
            rm -rf $repoUpdateDir
        fi
        echo `date` ": Repo update finished" >> $logFile

    elif [ "$updateType" == "FW_UPDATE_ARCHIVE" ]
    then
        echo `date` ": Archive Update found" >> $logFile
        if [ -e "$archiveUpdatePath" ]
        then
            echo `date` ": Archive update file exists" >> $logFile
            rm -rf /tmp/fwUpgrade
            mkdir /tmp/fwUpgrade
            unzip -d /tmp/fwUpgrade $archiveUpdatePath
            currentVer=`cat $fwPath/version.info | xargs`
            newVer=`cat /tmp/fwUpgrade/WBEGATEWAY-master/version.info | xargs`
            if [ "$newVer" -gt "$currentVer" ]
            then
                echo `date` ": New version is higher than current version, Update will be applied" >> $logFile
                rm -rf $fwPath
                mkdir $fwPath
                cp -r /tmp/fwUpgrade/WBEGATEWAY-master/* $fwPath/
            fi
            rm -rf /tmp/fwUpgrade
            rm $archiveUpdatePath
            rm $upgInfoFile
        fi
        echo `date` ": Archive Firmware update finished" >> $logFile
    elif [ "$updateType" == "MODBUS_CONFIG_UPDATE" ]
    then
        echo `date` ": Modbus Config update found" >> $logFile
        if [ -e "$modbusConfigUpdatePath" ]
        then
            echo `date` ": Modbus config Update file exists" >> $logFile
            cp $modbusConfigUpdatePath"/"$deviceId"/modbus_dev/devices.json" $modbusConfigFile
            rm $modbusConfigUpdatePath
            rm $upgInfoFile
        fi
        echo `date` ": Modbus Config Update finished" >> $logFile
    elif [ "$updateType" == "MAIN_CONFIG_UPDATE" ]
    then
        echo `date` ": Main config update found" >> $logFile
        if [ -e "$mainConfigUpdatePath" ]
        then
            echo `date` ": Main config update file exists" >> $logFile
            cp $mainConfigUpdatePath"/"$deviceId"/config/config.json" $mainConfigFile
            rm $mainConfigUpdatePath
            rm $upgInfoFile
        fi
        echo `date` ": Main config update finished" >> $logFile
    fi
fi
