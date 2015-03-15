#!/usr/bin/env python

import subprocess, os, signal, sys, re
from time import *
from config import *

def launchvideo(url):

	if is_running("omxplayer.bin") == True : 
		os.system("killall omxplayer.bin")

	os.system("cat images/url.asc | wall")

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

	print "Full video URL is : ", out	
	#os.system('echo "Video link is: ' + out + '" | wall')
	out = out.rstrip()

	os.system("cat images/omx.asc | wall")

	omx = "omxplayer -b -o "+audio_output+" '"+out+"' < /tmp/cmd"

	os.system(omx+" &")

	os.system("echo . > /tmp/cmd")

def is_running(process):
        s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        for x in s.stdout:
                if re.search(process, x):
                        return True
        return False
