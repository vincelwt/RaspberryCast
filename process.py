import youtube_dl
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

import os, threading
from config import *
#import YoutubeFullUrl
import logging
logger = logging.getLogger(" | RaspberryCast | ")

def launchvideo(url, sub, slow):
	setState("2")

	if new_log == True:
		os.system("sudo fbi -T 1 -a --noverbose images/processing.jpg &")

	logger.info('CASTING: Trying to retrieve source video URL...')	

	out = return_full_url(url, sub, slow)

	logger.debug("CASTING: Full video URL fetched. Sarting OMXPlayer now.")
	
	thread = threading.Thread(target=playWithOMX, args=(out, sub,))
	thread.start()
	
	#Start signal for OMXplayer
	os.system("echo . > /tmp/cmd")

def return_full_url(url, sub, slow):
	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True):	
		logger.info('CASTING: Direct video URL, no need to use youtube-dl.')
		return url

	"""
	if ("youtu" in url) and (slow == False):
		logger.debug('CASTING: Youtube link detected, extracting url in maximal quality.')
		return YoutubeFullUrl.get_flux_url(url) #A lot faster than youtube-dl, but doesn't works on very large videos """

	with ydl: #Downloading youtub-dl infos
	    result = ydl.extract_info(
	        url,
	        download=False # We just want to extract the info
	    )

	if 'entries' in result: # Can be a playlist or a list of videos
	    video = result['entries'][0]
	else:
	    video = result # Just a video

	if "youtu" in url:
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
		logger.debug('CASTING: Video not from Youtube or Vimeo. Extracting url in maximal quality.')
		return video['url']

def playWithOMX(url, sub):
	setState("1")
	if sub == True:
		os.system("omxplayer -b -r -o both '" + url + "' --subtitles subtitle.srt < /tmp/cmd")
		os.remove("subtitle.srt")
	else :
		os.system("omxplayer -b -r -o both '" + url + "' < /tmp/cmd")
	setState("0")
	#Check if playlist is empty or not	
	with open('video.queue', 'r') as f:
		first_line = f.readline()
		if first_line != "":
			logger.info("Starting next from video.queue : "+first_line)
			with open('video.queue', 'r') as fin:
				data = fin.read().splitlines(True)
			with open('video.queue', 'w') as fout:
				fout.writelines(data[1:])
			launchvideo(first_line, False, False)
		else:
			logger.debug("No links in video.queue, skipping.")
			if new_log == True:
				os.system("sudo fbi -T 1 -a --noverbose images/ready.jpg &")

def setState(state):
	os.system("echo "+state+" > state.tmp") #Write to file so it can be accessed from everywhere
