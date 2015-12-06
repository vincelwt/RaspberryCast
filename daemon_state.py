#!/usr/bin/env python

import re, os, subprocess
from process import *
import threading
from time import sleep

import logging
logger = logging.getLogger(" | RaspberryCast | ")


"""
f = open('RaspberryCast.log', 'r')
size = os.path.getsize('RaspberryCast.log')

while 1:
    #Log management
	if os.path.getsize('RaspberryCast.log') == size:
		line = f.readline()
		if line:
			print "Log: " + line
				size = os.path.getsize('RaspberryCast.log')
		sleep(0.2)"""

def StartDialogLog() :
	thread = threading.Thread(target=DialogLog)
	thread.start()
	return "ok"

def DialogLog() :
	begin = state()
	os.system("dialog --title RaspberryCast --infobox \"Use the Chrome extension, the web app, or the Android app to stream content.\" 5 50")
	while 1:
		now = state()
		if now != begin :
			if now == "0" :
				os.system("dialog --title RaspberryCast --infobox \"Use the Chrome extension, the web app, or the Android app to stream content.\" 5 50")
			elif now == "1" :
				os.system("dialog --title RaspberryCast --infobox \"Media should now be playing !\" 5 50")
			elif now == "2" :
				os.system("dialog --title RaspberryCast --infobox \"Processing media with youtube-dl...\n\nRetrieving source video URL before playing...\n\nCan take up to 40s with slow connections.\" 7 50")
			begin = now
		sleep(0.2)
	
def state():
	running_omx = checkprocess("omxplayer.bin")
	running_yt = checkprocess("youtube-dl")
	if running_omx == True:
		return "1"
	elif running_yt == True:
		return "2"
	else:
		return "0"

def checkprocess(process):
        s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        for x in s.stdout:
                if re.search(process, x):
                        return True
	return False
