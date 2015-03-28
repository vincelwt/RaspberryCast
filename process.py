#!/usr/bin/env python

import subprocess, os, signal, sys, re
from time import *
from config import *
import logging

def launchvideo(url, sub):
	try :
		os.system("echo -ne '\033[9;0]' >/dev/tty1")
	except :
		logging.error('Unable to wake up screen. Giving up.')

	if is_running() == True : 
		os.system("killall omxplayer.bin")

	#os.system("cat images/url.asc | wall")
	logging.info('Trying to retrieve video URL...')
	

	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True) :	
		print "No need to Youtube-dl."	
		logging.info('Direct file, no need to youtube-dl.')
		out = url
		
	else :
		if low_mode == True:
			logging.info('Fast mode enabled (360p).')
			if url[0:14] in ("https://youtu.", "http://youtu.b", "https://www.yo", "http://www.you", "http://youtub", "http://youtube") :
				print "Youtube, setting to 360p"
				command = "youtube-dl -f 18 -g "
			elif url[0:12] in ("https://vime", "http://vimeo") :
				print "Vimeo, setting to 360p"
				command = "youtube-dl -f h264-sd -g "
			else :
				command = "youtube-dl -g "
		else:
			logging.info('Normal mode, trying to extract full url.')
			print "Trying to extract full url..."
			command = "youtube-dl -g "

	
		try :
			proc = subprocess.Popen(command+url, stdout=subprocess.PIPE, shell=True)

			(out, err) = proc.communicate()
		except :
			logging.error('Error with youtube-dl. Giving up.')
		
		out = out.rstrip()

	logging.info("Full video URL is : " + out)	

	#os.system("cat images/omx.asc | wall")
	logging.info("Trying to start OMX")
	
	if sub == True :
		logging.info('Starting OMX with subtitles.')
		omx = "omxplayer -b -o "+sound_output+" '"+out+"' --subtitles subtitle.srt < /tmp/cmd"
		
	else :
		logging.info('Starting OMX without subtitles.')
		omx = "omxplayer -b -o "+sound_output+" '"+out+"' < /tmp/cmd"
			

	try :
		os.system(omx+" &")
	except :
		logging.error('Unable to start OMX. Giving up.')

	os.system("echo . > /tmp/cmd")

def is_running():
        s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        for x in s.stdout:
                if re.search("omxplayer.bin", x):
                        return True
	return False

