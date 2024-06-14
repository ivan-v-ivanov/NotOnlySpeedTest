#!/bin/bash

while true
do

	bot_pid=`ps -eo pid,cmd | grep botstart.sh | grep -v grep | awk {'print $1'} | head -1`
	if [[ -n $bot_pid ]]; then
		kill $bot_pid
		echo "SUCCESS: bot (PID $bot_pid) was found and terminated by killbot"

	else
		break
	fi
done
