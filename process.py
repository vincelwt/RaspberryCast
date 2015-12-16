import youtube_dl
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

import os, threading
from config import *
#import YoutubeFullUrl
import logging
logger = logging.getLogger("RaspberryCast")

def launchvideo(url, sub, slow):
	setState("2")
	os.system("echo -n q > /tmp/cmd &")
	if new_log == True:
		os.system("sudo fbi -T 1 -a --noverbose images/processing.jpg &")

	logger.info('Extracting source video URL...')	
	out = return_full_url(url, sub, slow)
	logger.debug("Full video URL fetched.")
	
	thread = threading.Thread(target=playWithOMX, args=(out, sub,))
	thread.start()
	
	os.system("echo . > /tmp/cmd") #Start signal for OMXplayer

def queuevideo(url, slow):
	logger.info('Extracting source video URL, before adding to queue...')	

	out = return_full_url(url, False, slow)

	logger.info("Full video URL fetched.")

	if getState() == 0:
		logger.info('No video currently playing, playing video instead of adding to queue.')
		thread = threading.Thread(target=playWithOMX, args=(out, False,))
		thread.start()
	else:
		with open('video.queue', 'a') as f:
			f.write(out+'\n')

def return_full_url(url, sub, slow):
	logger.debug("Parsing source url for "+url+" with subs :"+str(sub)+" and slow mode :"+str(slow))

	if (url[-4:] in (".avi", ".mkv", ".mp4", ".mp3")) or (sub == True):	
		logger.debug('Direct video URL, no need to use youtube-dl.')
		return url

	with ydl: #Downloading youtub-dl infos
	    result = ydl.extract_info(url, download=False)# We just want to extract the info

	if 'entries' in result: # Can be a playlist or a list of videos
	    video = result['entries'][0]
	else:
	    video = result # Just a video

	if "youtu" in url:
		if slow == True:
			for i in video['formats']:
				if i['format_id'] == "18":
					logger.debug("Youtube link detected, extracting url in 360p")
					return i['url']
		else:
			logger.debug('CASTING: Youtube link detected, extracting url in maximal quality.')
			return video['url']
	elif "vimeo" in url:
		if slow == True:
			for i in video['formats']:
				if i['format_id'] == "http-360p":
					logger.debug("Vimeo link detected, extracting url in 360p")
					return i['url']
		else:
			logger.debug('Vimeo link detected, extracting url in maximal quality.')
			return video['url']
	else :
		logger.debug('Video not from Youtube or Vimeo. Extracting url in maximal quality.')
		return video['url']

def playWithOMX(url, sub):
	logger.info("Sarting OMXPlayer now.")

	setState("1")
	if sub == True:
		os.system("omxplayer -b -r -o both '" + url + "' --subtitles subtitle.srt < /tmp/cmd")
		os.remove("subtitle.srt")
	else :
		os.system("omxplayer -b -r -o both '" + url + "' < /tmp/cmd")
	
	if getState() != "2": # In case we are again in the launchvideo function
		setState("0")
		with open('video.queue', 'r') as f: #Check if there is videos in queue
			first_line = f.readline().replace('\n', '')
			if first_line != "":
				logger.info("Starting next video in playlist.")
				with open('video.queue', 'r') as fin:
					data = fin.read().splitlines(True)
				with open('video.queue', 'w') as fout:
					fout.writelines(data[1:])
				thread = threading.Thread(target=playWithOMX, args=(first_line, False,))
				thread.start()
				os.system("echo . > /tmp/cmd") #Start signal for OMXplayer
			else:
				logger.debug("No links in video.queue, skipping.")
				if new_log == True:
					os.system("sudo fbi -T 1 -a --noverbose images/ready.jpg &")

def setState(state):
	os.system("echo "+state+" > state.tmp") #Write to file so it can be accessed from everywhere

def getState():
	with open('state.tmp', 'r') as f:
		return f.read().replace('\n', '')