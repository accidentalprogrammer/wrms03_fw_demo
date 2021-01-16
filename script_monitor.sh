#!/bin/bash

logpath=/fw
_date=`date`
is_data_logger=`sudo ps -aux | grep -c 'DataLoggerMain'`                #This outputs 2, when the process is running. 1 for the process name found and one for the grep command found, which now becomes the process.
echo $is_data_logger
if [ "$is_data_logger" -eq "1" ]
then
    echo $is_data_logger
    echo $_date "Restarting 'DataLoggerMain.py' script." >> $logpath/ps_watch.log
    sudo python3 /fw/DataLogger/app/DataLoggerMain.py &
fi
