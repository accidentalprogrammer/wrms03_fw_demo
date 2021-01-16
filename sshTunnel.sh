#!/bin/bash


sshStatus=`cat /root/sshStatus | xargs`
echo $sshStatus
if [ "$sshStatus" = "CONNECT" ]; then
	for number in `ps -x | grep sshForwarding.py | sed --expression 's/^ *//' | cut -f1 -d' '`; do kill $number; done
	echo "Connect the SSH"
	rm /root/sshStatus
	python3 /root/DataLogger/app/sshForwarding.py &
elif [ "$sshStatus" = "DISCONNECT" ]; then
	echo "Disconnect the SSH"
	for number in `ps -x | grep sshForwarding.py | sed --expression 's/^ *//' | cut -f1 -d' '`; do kill $number; done
fi
