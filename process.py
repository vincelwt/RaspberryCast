#!/usr/bin/env python

import subprocess, os, signal, sys, re
from time import *
from config import *
import logger

def launchvideo(url, sub):
	try :
		os.system("echo -ne '\033[9;0]' >/dev/tty1")
	except :
		logger.error('CASTING: Unable to wake up screen. Giving up.')

	if is_running() == True : 
		logger.info('CASTING: OMXPlayer already running, killing previous instance.')
		os.system("killall omxplayer.bin")

	#os.system("cat images/url.asc | wall")
	logger.info('CASTING: Trying to retrieve video URL...')
	

	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True) :	
		logger.info('CASTING: Direct video URL, no need to use youtube-dl.')
		out = url
		
	else :
		if low_mode == True:
			logger.info('CASTING: Fast mode enabled (360p).')
			if url[0:14] in ("https://youtu.", "http://youtu.b", "https://www.yo", "http://www.you", "http://youtub", "http://youtube") :
				logger.info("CASTING: Youtube link detected, setting to 360p")
				command = "youtube-dl -f 18 -g "
			elif url[0:12] in ("https://vime", "http://vimeo") :
				logger.info("CASTING: Vimeo link detected, setting to 360p")
				command = "youtube-dl -f h264-sd -g "
			else :
				command = "youtube-dl -g "
		else:
			logger.info('CASTING: Trying to extract full url in maximal quality.')
			command = "youtube-dl -g "

	
		try :
			proc = subprocess.Popen(command+url, stdout=subprocess.PIPE, shell=True)

			(out, err) = proc.communicate()
		except :
			logger.error('CASTING: Error with youtube-dl. Giving up.')
		
		out = out.rstrip()

	logger.info("CASTING: Full video URL is : " + out)	

	#os.system("cat images/omx.asc | wall")
	logger.info("CASTING: Sarting OMXPlayer now.")
	
	if sub == True :
		logger.info('CASTING: Starting OMX with subtitles.')
		omx = "omxplayer -b -r -o "+sound_output+" '"+out+"' --subtitles subtitle.srt < /tmp/cmd"
		
	else :
		logger.info('CASTING: Starting OMX without subtitles.')
		omx = "omxplayer -b -r -o "+sound_output+" '"+out+"' < /tmp/cmd"
			

	try :
		os.system(omx+" &")
	except :
		logger.error('CASTING: Unable to start OMX. Giving up.')

	os.system("echo . > /tmp/cmd &")

def is_running():
        s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        for x in s.stdout:
                if re.search("omxplayer.bin", x):
                        return True
	return False

