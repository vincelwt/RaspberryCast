#!/bin/sh

if [ $1 = "start" ]; then
	echo "Starting server."
	./server.py &
	
	echo "Starting queue daemon."
	./daemon_queue.py &
	
	exit
elif [ $1 = "stop" ] ; then
	if [ `id -u` -ne 0 ]
	then
	  echo "Please start this script with root privileges!"
	  echo "Try again with sudo."
	  exit 0
	fi
	
	echo "Killing RaspberryCast..."
	killall omxplayer.bin
	killall python
	kill $(lsof -t -i :2020)
	exit	

else 
	echo "Error, wrong argument. Try with 'stop' or 'start'. Don't forget the root privileges."
	exit
fi
