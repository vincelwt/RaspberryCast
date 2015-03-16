#!/usr/bin/env python

import subprocess, os, signal, sys, re
from time import *
from config import *

def launchvideo(url, sub):

	os.system("touch process.running")

	if is_running() == True : 
		os.system("killall omxplayer.bin")

	os.system("cat images/url.asc | wall")

	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True) :	
		print "No need to Youtube-dl."	
		out = url
		
	else :
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
			print "Trying to extract full url..."
			command = "youtube-dl -g "

	

		proc = subprocess.Popen(command+url, stdout=subprocess.PIPE, shell=True)

		(out, err) = proc.communicate()

		print "Full video URL is : ", out
		out = out.rstrip()

	os.system("cat images/omx.asc | wall")
	
	if sub == True :
		omx = "omxplayer -b -o "+audio_output+" '"+out+"' --subtitles subtitle.srt < /tmp/cmd"
	else :
		omx = "omxplayer -b -o "+audio_output+" '"+out+"' < /tmp/cmd"

	os.system(omx+" &")

	os.system("echo . > /tmp/cmd")
	
	os.system("rm process.running")

def popcorn(url):
	os.system("touch process.running")

	if is_running() == True : 
		os.system("killall omxplayer.bin")

	print "No need to Youtube-dl (PopcornTime)."	
	out = url

	os.system("cat images/url.asc | wall")

	omx = "omxplayer -b -o "+audio_output+" '"+out+"' --subtitles subtitle.srt < /tmp/cmd"

	os.system(omx+" &")
	os.system("echo . > /tmp/cmd")

	os.system("rm process.running")

def is_running():
	
        s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        for x in s.stdout:
                if re.search("omxplayer.bin", x):
                        return True
        if os.path.exists("process.running") == True:
		return True
	else :
		return False

