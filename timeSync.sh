#!/bin/bash

has_internet()
{
    ping -q  -w 30 -c 1 '8.8.8.8' > /dev/null && return 1 || return 0
}


has_internet
internet_connected=$?

if [ $internet_connected -eq 1 ]; then
    hwclock -f /dev/rtc1 -w
    hwclock -s -f /dev/rtc1
fi
