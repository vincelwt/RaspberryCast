#!/usr/bin/env python

<<<<<<< HEAD
import subprocess, os, signal, sys, re
from time import *
=======
import subprocess, os, signal, sys
from time import *
#from timeout import timeout
>>>>>>> ba9f1de9fc0c68e94a6866f9000f2cd20b7a37e5
from config import *

already_played = False

def launchvideo(url):
	
	global already_played
	
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

	#print "Program output is:", out	
	#os.system('echo "Video link is: ' + out + '" | wall')
	out = out.rstrip()
<<<<<<< HEAD

	if is_running("omxplayer.bin") == True : 
		os.system("killall omxplayer.bin")
	
	os.system("cat images/omx.asc | wall")

	omx = "omxplayer -b -o "+audio_output+" '"+out+"' < /tmp/cmd"
	omxplay = subprocess.Popen(omx, stdout=subprocess.PIPE, shell=True)
=======

	#trytostopRunning()
	os.system("killall omxplayer.bin")
	
	os.system("cat images/omx.asc | wall")

	omx = "omxplayer -b -o "+audio_output+" '"+out+"' < /tmp/cmd"
	omxplay = subprocess.Popen(omx, stdout=subprocess.PIPE, shell=True)

	os.system("echo . > /tmp/cmd")

#@timeout(3)
def trytostopRunning() :
	os.system("echo -n q > /tmp/cmd")
	print "Video was running"
	os.system("cat images/stop.asc | wall")
>>>>>>> ba9f1de9fc0c68e94a6866f9000f2cd20b7a37e5

	os.system("echo . > /tmp/cmd")

def is_running(process):
        s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        for x in s.stdout:
                if re.search(process, x):
                        return True
        return False
