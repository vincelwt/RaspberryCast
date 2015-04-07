#!/usr/bin/env python

import subprocess, os, signal, sys, re
from time import *
from config import *
from daemon_state import *
import logging
logger = logging.getLogger(" | RaspberryCast | ")

def launchvideo(url, sub):
	#Waking up screen
	try :
		os.system("echo -ne '\033[9;0]' >/dev/tty1")
	except :
		logger.error('CASTING: Unable to wake up screen. Giving up.')

	if state() == "1" : 
		logger.debug('CASTING: OMXPlayer already running, killing previous instance.')
		os.system("killall omxplayer.bin")
	elif state() == "2" : 
		logger.debug('CASTING: Youtube-dl already running, killing previous instance.')
		os.system("killall youtube-dl")

	#os.system("cat images/url.asc | wall")
	logger.info('CASTING: Trying to retrieve source video URL...')
	

	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True) :	
		logger.info('CASTING: Direct video URL, no need to use youtube-dl.')
		out = url
		
	else :
		if low_mode == True:
			logger.debug('CASTING: Fast mode enabled (360p).')
			if url[0:14] in ("https://youtu.", "http://youtu.b", "https://www.yo", "http://www.you", "http://youtub", "http://youtube") :
				logger.debug("CASTING: Youtube link detected, setting to 360p")
				command = "youtube-dl -f 18 -g "
			elif url[0:12] in ("https://vime", "http://vimeo") :
				logger.debug("CASTING: Vimeo link detected, setting to 360p")
				command = "youtube-dl -f h264-sd -g "
			else :
				command = "youtube-dl -g "
		else:
			logger.debug('CASTING: Trying to extract full url in maximal quality.')
			command = "youtube-dl -g "

	
		try :
			proc = subprocess.Popen(command+url, stdout=subprocess.PIPE, shell=True)

			(out, err) = proc.communicate()
		except :
			logger.error('CASTING: Error with youtube-dl. Giving up.')
		
		out = out.rstrip()

	logger.debug("CASTING: Full video URL is : " + out)	

	#os.system("cat images/omx.asc | wall")
	logger.info("CASTING: Sarting OMXPlayer now.")
	
	if sub == True :
		logger.debug('CASTING: Starting OMX with subtitles.')
		omx = "omxplayer -b -r -o "+sound_output+" '"+out+"' --subtitles subtitle.srt < /tmp/cmd"
		
	else :
		logger.debug('CASTING: Starting OMX without subtitles.')
		omx = "omxplayer -b -r -o "+sound_output+" '"+out+"' < /tmp/cmd"
			

	try :
		os.system(omx+" &")
	except :
		logger.error('CASTING: Unable to start OMX. Giving up.')

	os.system("echo . > /tmp/cmd &")
