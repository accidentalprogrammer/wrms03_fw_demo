#!/bin/bash

now="$(date)"
has_internet()
{
    #echo $_date" Start " >> /root/modemReset.log
    ping -q  -w 30 -c 1 '8.8.8.8' > /dev/null && return 1 || return 0
    #echo $_date" END " >> /root/modemReset.log
}

no_of_attempts=0
#now="$(date)"
echo "Script Started: $now"
while true
do
    has_internet
    has_internet_return_code=$?
    echo "return code = "$has_internet_return_code

    _date=`date`

    if [ $has_internet_return_code -eq 0 ]; then
        echo "inside if condition"
        echo $_date" No internet present. Hard resetting Modem." > /root/modemReset.log
        echo $apn
        sudo python3 /root/DataLogger/app/resetModem.py
        sleep 2

        if ( lsusb | grep '1e0e:9001' ); then
            #Now set up the modem again.
	    wvdial -C /root/DataLogger/config/wvdial.conf &
            sleep 5
        fi

    else
        echo "inside else condition"
        break;
    fi

    no_of_attempts=$((no_of_attempts+1))
    if [ $no_of_attempts -eq 3 ]; then
        break;
    else
        sleep 60
    fi

done
