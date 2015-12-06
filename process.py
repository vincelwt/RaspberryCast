#!/usr/bin/env python

import os
import youtube_dl
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

#from time import *
from config import *
import YoutubeFullUrl
from daemon_state import *
import logging
logger = logging.getLogger(" | RaspberryCast | ")

def launchvideo(url, sub, slow):
	#Waking up screen
	os.system("echo -ne '\033[9;0]' >/dev/tty1")

	if state() == "1" : 
		logger.debug('CASTING: OMXPlayer already running, killing previous instance.')
		os.system("killall omxplayer.bin")
	elif state() == "2" : 
		logger.debug('CASTING: Youtube-dl already running, killing previous instance.')
		os.system("killall youtube-dl")

	logger.info('CASTING: Trying to retrieve source video URL...')	

	out = return_full_url(url, sub, slow)

	#logger.debug("CASTING: Full video URL fetched.")
	logger.debug("CASTING: Full video URL is : " + out)	

	logger.info("CASTING: Sarting OMXPlayer now.")
	
	if sub == True :
		logger.debug('CASTING: Starting OMX with subtitles.')
		omx = "omxplayer -b -r -o both '"+out+"' --subtitles subtitle.srt < /tmp/cmd"
		
	else :
		logger.debug('CASTING: Starting OMX without subtitles.')
		omx = "omxplayer -b -r -o both '"+out+"' < /tmp/cmd"
			
	try :
		os.system(omx+" &")
	except :
		logger.error('CASTING: Unable to start OMX. Giving up.')

	os.system("echo . > /tmp/cmd &")

def return_full_url(url, sub, slow):
	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True):	
		logger.info('CASTING: Direct video URL, no need to use youtube-dl.')
		return url

	"""
	if ("youtu" in url) and (slow == False):
		logger.debug('CASTING: Youtube link detected, extracting url in maximal quality.')
		return YoutubeFullUrl.get_flux_url(url) #A lot faster than youtube-dl """

	with ydl: #Downloading youtub-dl infos
	    result = ydl.extract_info(
	        url,
	        download=False # We just want to extract the info
	    )

	if 'entries' in result: # Can be a playlist or a list of videos
	    video = result['entries'][0]
	else:
	    video = result # Just a video

	if "youtu" in url == True:
		if slow == True:
			for i in video['formats']:
				if i['format_id'] == "18":
					logger.debug("CASTING: Youtube link detected, extracting url in 360p")
					return i['url']
		else:
			logger.debug('CASTING: Youtube link detected, extracting url in maximal quality.')
			return video['url']
	elif "vimeo" in url:
		if slow == True:
			for i in video['formats']:
				if i['format_id'] == "http-360p":
					logger.debug("CASTING: Vimeo link detected, extracting url in 360p")
					return i['url']
		else:
			logger.debug('CASTING: Vimeo link detected, extracting url in maximal quality.')
			return video['url']
	else :
		return video['url']
