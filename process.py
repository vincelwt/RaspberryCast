#!/usr/bin/env python

import subprocess, os, signal, sys
from config import *

already_played = False

def launchvideo(url):
	
	global already_played

	os.system("fim images/url.gif &")

	if low_mode == True:
		if url[0:14] in ("https://youtu.", "http://youtu.b", "https://www.yo", "http://www.you", "http://youtub", "http://youtube") :
			print "Youtube, setting to 360p"
			command = "youtube-dl -f 18 -g "
		elif url[0:12] in ("https://vime", "http://vimeo") :
			print "Vimeo, setting to 360p"
			command = "youtube-dl -f h264-sd -g "
		else :
			command = "youtube-dl -g "
	else:
		command = "youtube-dl -g "

	proc = subprocess.Popen(command+url, stdout=subprocess.PIPE, shell=True)

	(out, err) = proc.communicate()

	#print "Program output is:", out	
	#os.system('echo "Video link is: ' + out + '" | wall')
	out = out.rstrip()

	if already_played == True:
		print "Subprocess already running"
		os.system("echo -n q > /tmp/cmd")

	os.system("fim images/url.gif &")
	omx = "omxplayer -b -o "+audio_output+" '"+out+"' < /tmp/cmd"
	omxplay = subprocess.Popen(omx, stdout=subprocess.PIPE, shell=True)
	already_played = True
	os.system("echo . > /tmp/cmd")	


# Methods that can be used to kill the process
#	os.system("echo -n q > /tmp/cmd")
#	os.killpg(omxplay.pid, signal.SIGTERM)
#	os.system("killall omxplayer.bin")

