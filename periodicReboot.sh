#!/bin/bash


prevDate=`cat /fw/lastDate`
currentDate=`date +%d`
lastTime=1569062178
curTime=`date +%s`
if [[ -z $prevDate ]]; then
	prevDate=$currentDate
fi

if [ $curTime -gt $lastTime ]; then
    echo $currentDate > /fw/lastDate
    if [ "$prevDate" != "$currentDate" ]; then
        sudo reboot
    fi
fi
