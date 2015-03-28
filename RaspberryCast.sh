#!/bin/sh
cd /home/pi/RaspberryCast/

if [ $1 = "start" ]; then
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
	echo "Starting server."
	su - pi -c "/home/pi/RaspberryCast/server.py &"
	su - pi -c "/home/pi/RaspberryCast/daemon_queue.py &"
	echo "Done."
	exit


else
	echo "Error, wrong argument. Try with 'stop' or 'start'."
	exit
fi
