#!/bin/sh
cd /home/pi/RaspberryCast/

if [ $1 = "start" ]; then
	if [ `id -u` -eq 0 ]
	then
		echo "Please start this script without root privileges!"
		echo "Try again without sudo."
		exit 0
	fi
	echo "Starting server."
	./server.py &
	./daemon_queue.py &
	echo "Done."
	exit
elif [ $1 = "stop" ] ; then
	if [ `id -u` -ne 0 ]
	then
		echo "Please start this script with root privileges!"
		echo "Try again with sudo."
		exit 0
	fi
	echo "Killing RaspberryCast..."
	killall omxplayer.bin >/dev/null 2>&1
	killall python >/dev/null 2>&1
	kill $(lsof -t -i :2020) >/dev/null 2>&1
	rm *.pyc >/dev/null 2>&1
	rm *.srt >/dev/null 2>&1
	echo "Done."
	exit
elif [ $1 = "restart" ] ; then
        ./RaspberryCast.sh stop
        su - pi -c "./RaspberryCast.sh start"
else
	echo "Error, wrong argument. Try with 'stop', 'start' or 'restart'."
	exit
fi
